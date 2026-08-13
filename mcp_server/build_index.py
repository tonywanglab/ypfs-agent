"""Build the BM25 section index and (optionally) run a smoke query.

The server builds its index lazily in-process, so this is mainly a quick way to
verify the corpus is indexable and to sanity-check ranking from the CLI:

  python -m mcp_server.build_index                       # build + report counts
  python -m mcp_server.build_index --smoke "lender of last resort"
  python -m mcp_server.build_index --smoke "..." --document-type survey
"""

import argparse

from .index import get_index


def main() -> None:
    parser = argparse.ArgumentParser(description="Build/smoke-test the BM25 section index")
    parser.add_argument("--smoke", metavar="QUERY", help="run a sample search and print results")
    parser.add_argument("--document-type", help="filter the smoke query by document_type")
    parser.add_argument("--limit", type=int, default=5, help="max results for the smoke query")
    args = parser.parse_args()

    index = get_index()
    docs = {s["doc_id"] for s in index.sections}
    print(f"Indexed {len(index.sections)} sections across {len(docs)} documents.")

    if args.smoke:
        out = index.search(args.smoke, document_type=args.document_type, limit=args.limit)
        print(f"\nQuery: {args.smoke!r}  (total_found={out['total_found']})")
        for i, r in enumerate(out["results"], 1):
            crumb = " > ".join(r["section_path"]) or "(top)"
            print(f"\n{i}. [{r['score']}] {r['doc_id']} — {r['document_type']}")
            print(f"   {crumb}")
            snippet = r["text"].replace("\n", " ")[:200]
            print(f"   {snippet}...")


if __name__ == "__main__":
    main()
