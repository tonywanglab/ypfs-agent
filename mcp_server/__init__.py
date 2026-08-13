"""Local lexical (BM25) MCP server over the financial-crisis corpus.

A self-contained, embedding-free alternative to the Pinecone/pgvector RAG path:
it splits markdown/ into header-delimited sections, ranks them with BM25, and
exposes search_corpus / get_document / list_documents over MCP (stdio).
"""
