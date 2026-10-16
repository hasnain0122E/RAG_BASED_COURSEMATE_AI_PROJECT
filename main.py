from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

embeddings = OpenAIEmbeddings(model = "text-embedding-3-large")

llm = ChatOpenAI(model="gpt-4-0613")

vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 4,
        'fetch_k': 10,
        'lambda_mult': 0.5
    }
)

#prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system', """You are a helpful assistant. Your task is to answer questions about the context provided. If the question cannot be answered with the context provided, you should say 'I don't know'."""
        ),
        (
            'human', """Context: {context} Question: {question}"""
        )
    ]
)


print('======== RAG SYSTEM CHATBOT =========')
print('Press 0 to quit')

while True:
    query = input('You: ')
    if query == '0':
        break

    docs = retriever.invoke(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    final_prompt = prompt.invoke({
        'context': context,
        'question': query
    })

    response = llm.invoke(final_prompt)

    print('Assistant:', response.content)





