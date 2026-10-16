from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

docs = [
    Document(page_content="Gradient descent is an optimization algorithm used in machine learning."),
    Document(page_content="Gradient descent minimizes the loss function."),
    Document(page_content="Gradient descent is an optimization that minimizes the loss function."),
    Document(page_content="Neural networks use gradient descent for training."),
    Document(page_content="Support Vector Machines are supervised learning algorithms.")
]

embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(docs, embeddings)

similarity_retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},
)

print('================== Similarity Retriever ==================')

similarity_doc = similarity_retriever.invoke("What is gradient descent?")

for doc in similarity_doc:
    print(doc.page_content)

mmr_retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3},
)

print('================== MMR Retriever ==================')

mmr_doc = mmr_retriever.invoke("What is gradient descent?")

for doc in mmr_doc:
    print(doc.page_content)
