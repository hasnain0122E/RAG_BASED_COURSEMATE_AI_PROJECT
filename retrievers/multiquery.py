from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from dotenv import load_dotenv
load_dotenv()

data = [
    Document(page_content="Gradient descent is an optimization algorithm used in machine learning."),
    Document(page_content="Gradient descent minimizes the loss function."),
    Document(page_content="Gradient descent is an optimization that minimizes the loss function."),
    Document(page_content="Neural networks use gradient descent for training."),
    Document(page_content="Support Vector Machines are supervised learning algorithms.")
]


vectorstore = Chroma.from_documents(data, OpenAIEmbeddings())

retriever  = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

llm = ChatOpenAI(model="gpt-4-0613")

multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=llm,
)

query = "What is gradient descent?"

docs = multi_query_retriever.invoke(query)

for doc in docs:
    print(doc.page_content)
