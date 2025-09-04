from search_with_document_layout import DocumentRAGSearch

if __name__ == "__main__":
    rag = DocumentRAGSearch()

    rag.split_documents_into_chunks()

    # embed and index the docs:
    vector_store = rag.embed_and_index_chunks()

    rag_chain = rag.setup_document_rag_chain(vector_store)
    while True:
        query = input("Enter your query: ")
        if query=="":
            break
        rag.document_search(rag_chain, query)