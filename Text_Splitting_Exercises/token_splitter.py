
import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter

article = """
Retrieval-Augmented Generation (RAG) combines information retrieval
with large language models. A document is split into chunks, converted
into embeddings, and stored in a vector database. When a user asks a
question, relevant chunks are retrieved and passed to the language model.
""" * 30

splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base",
    chunk_size=200, chunk_overlap=30
)

chunks = splitter.split_text(article)

encoding = tiktoken.get_encoding("cl100k_base")

for i, chunk in enumerate(chunks, start=1):
    token_count = len(encoding.encode(chunk))
    print(f"Chunk {i}: {token_count} tokens")

    assert token_count <= 200

print("All chunks are within the token limit.")

