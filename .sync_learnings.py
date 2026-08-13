"""One-shot: splice LEARNINGS.md into README.md, demoting headings one level."""
from pathlib import Path

learnings = Path("LEARNINGS.md").read_text().splitlines()
readme = Path("README.md").read_text().splitlines()

out, in_fence = [], False
for line in learnings:
    if line.startswith("```"):
        in_fence = not in_fence
        out.append(line)
        continue
    out.append(("#" + line) if (not in_fence and line.startswith("#")) else line)

assert out[0] == "## What I learned building the YPFS crisis-analyst agent", out[0]
out[0] = "## Project wrap-up — what I learned"
# Intro paragraph carries the backlink; append it to that line.
out[2] += " Also kept standalone as [`LEARNINGS.md`](LEARNINGS.md)."

start = readme.index("## Project wrap-up — what I learned")
end = readme.index("## Ingestion Pipeline")
Path("README.md").write_text("\n".join(readme[:start] + out + ["", "---", ""] + readme[end:]) + "\n")
print(f"replaced README lines {start + 1}..{end} with {len(out)} lines")
