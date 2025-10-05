from django.contrib.auth.models import User
from ..models import Document
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from .chunk_document import chunk_document
from .extract_topics import extract_topics_and_subtopics
from .load_document import load_document
embeddings = OpenAIEmbeddings()


def document_ingest_node(state):
    """
    Input: state['file_path'], state['uploader_id']
    Output: state['doc_id'], state['topics'], state['status']
    """
    uploader = User.objects.get(id=state["uploader_id"])
    doc_instance = Document.objects.create(title=state.get("title", "Untitled"), uploader=uploader, status="processing")
    
    docs = load_document(state["file_path"])

    chunks = chunk_document(docs)

    topics_data = extract_topics_and_subtopics(docs, doc_instance)
    texts = [chunk.page_content for chunk in chunks]
    vector_store = FAISS.from_texts(texts, embeddings)
    vector_store.save_local(f"faiss_index_{doc_instance.doc_id}")

    doc_instance.status = "completed"
    doc_instance.save()

    return {
        "doc_id": doc_instance.doc_id,
        "topics": topics_data,
        "status": "parsed"
    }