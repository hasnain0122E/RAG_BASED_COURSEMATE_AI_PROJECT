from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

documents = [
    Document(
        page_content="Python is widely used in AI development. " * 20,
        metadata={"source": "python_guide.txt", "topic": "Python"},
    ),
    Document(
        page_content="FastAPI helps developers build APIs for AI models. " * 20,
        metadata={"source": "fastapi_guide.txt", "topic": "FastAPI"},
    ),
    Document(
        page_content="Large language models generate text using learned patterns. " * 20,
        metadata={"source": "llm_guide.txt", "topic": "LLMs"},
    )
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 200,
    chunk_overlap = 30
)

chunks = splitter.split_documents(documents)

print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {i} ---")
    print('Source', chunk.metadata.get('source'))
    print('Topic', chunk.metadata.get('topic'))
    print('Characters', len(chunk.page_content))
    print('Content', chunk.page_content)

    assert "source" in chunk.metadata
    assert "topic" in chunk.metadata

print('\n All chunks have been verified.')
