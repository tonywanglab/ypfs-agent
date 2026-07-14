from __future__ import annotations

from harness import registry, reviews, router
from harness.models import SupervisorReview


def test_create_and_load_review(evals_dir):
    review = reviews.create_review(
        "run_abc", verdict="unacceptable", primary_problem="missed options",
        failure_attribution="agent_failure", notes="needs work",
    )
    loaded = reviews.load_review(review.review_id)
    assert loaded.run_id == "run_abc"
    assert loaded.verdict == "unacceptable"
    assert loaded.failure_attribution == "agent_failure"
    assert loaded.notes == "needs work"


def test_list_and_filter_reviews(evals_dir):
    r1 = reviews.create_review("run_1", "unacceptable", "p", "agent_failure")
    reviews.create_review("run_2", "acceptable", "", "ambiguous")
    reviews.create_review("run_1", "unacceptable", "p2", "rubric_gap")

    assert len(reviews.list_reviews()) == 3
    assert len(reviews.reviews_for_run("run_1")) == 2
    assert reviews.reviews_by_attribution("agent_failure") == [r1]


def test_route_review_queues_on_branch_conflict(evals_dir):
    review = reviews.create_review("run_x", "unacceptable", "gap", "rubric_gap")
    registry.lock_cycle("prompt")

    status = router.route_review(review)
    assert status["queued"] is True
    assert status["branch"] == "rubric"
    assert review.review_id in registry.pending_queue()["rubric"]


def test_route_review_ready_when_unlocked(evals_dir):
    review = reviews.create_review("run_y", "unacceptable", "bad agent", "agent_failure")
    status = router.route_review(review)
    assert status == {"action": "ready", "branch": "prompt", "queued": False}


def test_route_acceptable_review_is_noop(evals_dir):
    review = reviews.create_review("run_z", "acceptable", "", "ambiguous")
    assert router.route_review(review) == {"action": "none", "branch": None, "queued": False}


def test_branch_for_attribution():
    assert router.branch_for_attribution("agent_failure") == "prompt"
    assert router.branch_for_attribution("rubric_gap") == "rubric"
    assert router.branch_for_attribution("ambiguous") is None
