from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader

def load_document(file_path: str):
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".docx"):
        loader = UnstructuredWordDocumentLoader(file_path)
    else:
        raise ValueError("Unsupported file type")
    return loader.load()

    # Load through dotsocr VLLM.
