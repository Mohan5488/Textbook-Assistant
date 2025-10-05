from ..models import Topic, SubTopic
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import json

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

def extract_topics_and_subtopics(documents, doc_instance):
    """
    Extract all topics and subtopics from textbook-like content using LLM.
    Saves them to DB and returns structured data.
    """
    combined_text = "\n\n".join([doc.page_content for doc in documents[:10]]) 

    prompt = (
        "You are an academic content analyzer. "
        "Read the following textbook content and extract a detailed list of topics. "
        "Each topic should include: title, page_start, page_end, summary, prerequisites, and subtopics.\n\n"
        "Return valid JSON ONLY in this exact format:\n\n"
        "[\n"
        "  {\n"
        "    'title': 'Chapter 1 – Introduction to Biology',\n"
        "    'page_start': 1,\n"
        "    'page_end': 10,\n"
        "    'summary': 'An overview of biological concepts and the study of life.',\n"
        "    'prerequisites': ['Basic science knowledge', 'Understanding of chemistry'],\n"
        "    'subtopics': [\n"
        "       {\n"
        "         'title': 'Cell Theory',\n"
        "         'summary': 'Describes the concept that all living things are made of cells.',\n"
        "         'page_start': 2,\n"
        "         'page_end': 3\n"
        "       }\n"
        "    ]\n"
        "  }\n"
        "]\n\n"
        f"Text content:\n{combined_text}\n\n"
        "Respond ONLY in strict JSON format."
    )

    response = llm.invoke(prompt)
    response_text = response.content
    print("----LLM Raw Response----")
    print(response_text)

    import re, json
    json_match = re.search(r'```(?:json)?\s*(.*?)\s*```', response_text, re.DOTALL)
    json_str = json_match.group(1).strip() if json_match else response_text.strip()

    json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        repaired = json_str.replace("'", '"')
        data = json.loads(repaired)

    print("----Parsed JSON Topics Count----", len(data))

    topics_list = []
    for i, item in enumerate(data):
        topic_obj = Topic.objects.create(
            doc=doc_instance,
            title=item.get("title", f"Topic {i+1}"),
            page_start=item.get("page_start", i+1),
            page_end=item.get("page_end", i+1),
            summary=item.get("summary", ""),
            prerequisites=item.get("prerequisites", []),
        )

        subtopics_data = item.get("subtopics", [])
        subtopics_objs = []
        for j, subtopic in enumerate(subtopics_data):
            sub_obj = SubTopic.objects.create(
                topic=topic_obj,
                title=subtopic.get("title", f"Subtopic {j+1}"),
                page_start=subtopic.get("page_start", 0),
                page_end=subtopic.get("page_end", 0),
                summary=subtopic.get("summary", ""),
            )
            subtopics_objs.append(sub_obj)

        topics_list.append({
            "title": topic_obj.title,
            "page_start": topic_obj.page_start,
            "page_end": topic_obj.page_end,
            "summary": topic_obj.summary,
            "prerequisites": topic_obj.prerequisites,
            "subtopics": [s.title for s in subtopics_objs],
        })

    print(f"✅ Extracted {len(topics_list)} topics with subtopics successfully.")
    return topics_list
