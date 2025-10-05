from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_document(documents, chunk_size=400, chunk_overlap=40):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = splitter.split_documents(documents)
    print("------------CHUNKS CREATED-----------")
    return chunks