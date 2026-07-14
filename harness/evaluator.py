"""The evaluator: two isolated model calls per run, around the checklist.

Call 1 (generate_checklist) runs BEFORE any candidate answer is read: given
only the case prompt and the frozen rubric's *llm* criteria, it independently
searches the corpus and produces a case-specific checklist. Its own search
results are never treated as ground truth — they are context for call 2.

Deterministic criteria never need a checklist item; they are always
evaluated the same way via harness.checks and copied straight into the
Judgment, verbatim, without another model call.

Call 2 (judge_answer) is a single non-tool completion: given the answer,
normalized trace, checklist, evaluator search context, and deterministic
check results, it returns per-criterion verdicts for the checklist's *llm*
criteria only.
"""

from __future__ import annotations

import json

from agent.tools import TOOLS, dispatch

from . import llm
from .models import CheckResult, Checklist, ChecklistItem, CriterionVerdict, Judgment, Rubric
from .storage import new_id, now_iso
from .trace import NormalizedTrace, normalize_messages

CHECKLIST_SYSTEM_PROMPT = """\
You are an independent evaluation assistant for a financial-crisis policy \
research agent. You are NOT the agent being evaluated and you must not see \
its answer — only the question it will be asked. Your job is to turn a \
frozen rubric plus this question into a concrete, case-specific checklist \
BEFORE anyone answers it.

You have access to the same corpus search tools the agent uses \
(search_corpus, get_document). Use them to understand what evidence is \
actually available for this question, so your checklist items are grounded \
in what a well-answered response could realistically cover or cite — not \
abstract restatements of the rubric.

Rubric criteria you may ground checklist items in (use these criterion_ids \
exactly; do not invent new ones):
{rubric_criteria}

When you are done searching, respond with ONLY a JSON object of this exact \
shape (no prose, no markdown fences):
{{
  "items": [
    {{"criterion_id": "<one of the ids above>",
      "instruction": "<concrete, case-specific check>",
      "rationale": "<why this matters for this case>"}}
  ],
  "search_summary": "<1-3 sentences on what you found searching the corpus>"
}}
Produce 3-8 items. Every criterion_id must be one of the ids listed above.
"""

JUDGE_SYSTEM_PROMPT = """\
You are an independent judge for a financial-crisis policy research agent. \
You did not write the answer being judged. Score it strictly against the \
provided case-specific checklist, using the evaluator's own independent \
corpus search as context for spotting likely omissions — but do not treat \
that search as ground truth; the evaluator can miss documents too.

Respond with ONLY a JSON object of this exact shape (no prose, no markdown \
fences):
{
  "criteria": [
    {"criterion_id": "<id>", "verdict": "pass" | "fail" | "uncertain",
     "evidence": "<short quote or paraphrase>", "confidence": <0-1 float>}
  ],
  "summary": "<2-4 sentence overall assessment>",
  "failure_feedback": "<concrete, actionable feedback for the update loop; \
empty string if there is nothing actionable>"
}
Include exactly one entry per checklist item's criterion_id (dedupe if a \
criterion has multiple checklist items).
"""


def generate_checklist(case_prompt: str, case_id: str, rubric: Rubric, model: str) -> Checklist:
    """Call 1: isolated tool loop, no knowledge of any candidate answer."""
    llm_criteria = [c for c in rubric.criteria if c.check_type == "llm"]
    criteria_block = "\n".join(f"- {c.id}: {c.description}" for c in llm_criteria)
    system_prompt = CHECKLIST_SYSTEM_PROMPT.format(rubric_criteria=criteria_block)

    content, messages = llm.run_tool_loop(
        system_prompt=system_prompt,
        user_msg=f"Question to be answered by the agent:\n\n{case_prompt}",
        model=model,
        tools=TOOLS,
        dispatch_fn=dispatch,
    )

    parsed = llm.parse_json_object(content)
    valid_ids = {c.id for c in llm_criteria}
    items = [
        ChecklistItem(
            id=new_id("item"),
            criterion_id=i.get("criterion_id", ""),
            instruction=i.get("instruction", ""),
            rationale=i.get("rationale", ""),
        )
        for i in parsed.get("items", [])
        if i.get("criterion_id") in valid_ids
    ]

    evaluator_trace = normalize_messages(messages)
    doc_ids = sorted(evaluator_trace.retrieved_doc_ids | evaluator_trace.fetched_doc_ids)

    return Checklist(
        checklist_id=new_id("chk"),
        case_id=case_id,
        rubric_id=rubric.rubric_id,
        model=model,
        items=items,
        evaluator_search_summary=parsed.get("search_summary", ""),
        evaluator_doc_ids=doc_ids,
        created_at=now_iso(),
    )


def _deterministic_verdicts(rubric: Rubric, check_results: list[CheckResult]
                             ) -> dict[str, CriterionVerdict]:
    results_by_id = {r.check_id: r for r in check_results}
    verdicts: dict[str, CriterionVerdict] = {}
    for criterion in rubric.criteria:
        if criterion.check_type != "deterministic":
            continue
        result = results_by_id.get(criterion.deterministic_check)
        if result is None:
            continue
        verdicts[criterion.id] = CriterionVerdict(
            criterion_id=criterion.id,
            verdict="pass" if result.passed else "fail",
            evidence=result.evidence,
            confidence=1.0,
            source="deterministic",
        )
    return verdicts


def judge_answer(answer: str, normalized_trace: NormalizedTrace, checklist: Checklist,
                  rubric: Rubric, check_results: list[CheckResult], run_id: str,
                  model: str) -> Judgment:
    """Call 2: single non-tool completion, independent of call 1's messages."""
    deterministic_verdicts = _deterministic_verdicts(rubric, check_results)

    llm_criterion_ids = list(dict.fromkeys(i.criterion_id for i in checklist.items))
    llm_verdicts: dict[str, CriterionVerdict] = {}
    summary = ""
    failure_feedback = ""

    if llm_criterion_ids:
        payload = {
            "checklist_items": [
                {"criterion_id": i.criterion_id, "instruction": i.instruction}
                for i in checklist.items
            ],
            "evaluator_search_summary": checklist.evaluator_search_summary,
            "evaluator_doc_ids": checklist.evaluator_doc_ids,
            "agent_answer": answer,
            "agent_retrieved_doc_ids": sorted(normalized_trace.retrieved_doc_ids),
            "agent_fetched_doc_ids": sorted(normalized_trace.fetched_doc_ids),
            "deterministic_check_results": [
                {"check_id": r.check_id, "passed": r.passed, "evidence": r.evidence}
                for r in check_results
            ],
        }
        parsed = llm.chat_json(
            system_prompt=JUDGE_SYSTEM_PROMPT,
            user_prompt=json.dumps(payload, indent=2, default=str),
            model=model,
        )
        for c in parsed.get("criteria", []):
            cid = c.get("criterion_id")
            if cid in llm_criterion_ids:
                llm_verdicts[cid] = CriterionVerdict(
                    criterion_id=cid,
                    verdict=c.get("verdict", "uncertain"),
                    evidence=c.get("evidence", ""),
                    confidence=float(c.get("confidence", 0.5)),
                    source="llm",
                )
        summary = parsed.get("summary", "")
        failure_feedback = parsed.get("failure_feedback", "")

    ordered_ids = list(deterministic_verdicts.keys()) + [
        cid for cid in llm_criterion_ids if cid not in deterministic_verdicts
    ]
    criteria: list[CriterionVerdict] = []
    for cid in ordered_ids:
        if cid in deterministic_verdicts:
            criteria.append(deterministic_verdicts[cid])
        elif cid in llm_verdicts:
            criteria.append(llm_verdicts[cid])
        else:
            criteria.append(CriterionVerdict(
                criterion_id=cid, verdict="uncertain",
                evidence="Judge did not return a verdict for this criterion.",
                confidence=0.0, source="llm",
            ))

    return Judgment(
        judgment_id=new_id("judg"),
        run_id=run_id,
        checklist_id=checklist.checklist_id,
        model=model,
        criteria=criteria,
        summary=summary,
        failure_feedback=failure_feedback,
        created_at=now_iso(),
    )
