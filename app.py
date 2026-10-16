import os
import tempfile
import uuid

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

st.set_page_config(page_title="Chat with your PDF", page_icon="📄", layout="centered")

# ---------- Same prompt as main.py ----------
PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Your task is to answer questions about the "
            "context provided. If the question cannot be answered with the context "
            "provided, you should say 'I don't know'.",
        ),
        ("human", "Context: {context} Question: {question}"),
    ]
)


# ---------- Cached models (created once per server) ----------
@st.cache_resource
def get_models():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    llm = ChatOpenAI(model="gpt-4-0613")
    return embeddings, llm


# ---------- Ingestion (same logic as databaseingestion.py, per upload) ----------
def build_retriever(uploaded_file, embeddings):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        docs = PyPDFLoader(tmp_path).load()
    finally:
        os.remove(tmp_path)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # In-memory store with a unique collection per upload
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=f"pdf_{uuid.uuid4().hex}",
    )

    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 10, "lambda_mult": 0.5},
    )
    return retriever, len(docs), len(chunks)


# ---------- Session state ----------
st.session_state.setdefault("messages", [])
st.session_state.setdefault("retriever", None)
st.session_state.setdefault("file_key", None)
st.session_state.setdefault("doc_info", None)

if not os.getenv("OPENAI_API_KEY"):
    st.error("OPENAI_API_KEY not found. Add it to your .env file and restart.")
    st.stop()

embeddings, llm = get_models()

# ---------- Sidebar ----------
with st.sidebar:
    st.title("📄 Chat with your PDF")
    st.caption("Upload a PDF, then ask questions about it.")

    uploaded = st.file_uploader("Upload a PDF", type=["pdf"])

    if uploaded is not None:
        file_key = f"{uploaded.name}-{uploaded.size}"
        if st.session_state.file_key != file_key:
            with st.spinner("Reading and indexing your PDF..."):
                try:
                    retriever, n_pages, n_chunks = build_retriever(uploaded, embeddings)
                    st.session_state.retriever = retriever
                    st.session_state.file_key = file_key
                    st.session_state.doc_info = {
                        "name": uploaded.name,
                        "pages": n_pages,
                        "chunks": n_chunks,
                    }
                    st.session_state.messages = []  # fresh chat for a new document
                except Exception as e:
                    st.error(f"Could not process this PDF: {e}")

    if st.session_state.doc_info:
        info = st.session_state.doc_info
        st.success(f"Ready: **{info['name']}**")
        st.metric("Pages", info["pages"])
        st.metric("Chunks indexed", info["chunks"])

    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------- Main area ----------
st.header("Ask your document anything")

if st.session_state.retriever is None:
    st.info("👈 Upload a PDF in the sidebar to get started.")

# Render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📚 Sources"):
                for s in msg["sources"]:
                    st.markdown(f"**Page {s['page']}**")
                    st.caption(s["text"])

# Chat input
query = st.chat_input(
    "Ask a question about your PDF...",
    disabled=st.session_state.retriever is None,
)

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Searching the document..."):
            docs = st.session_state.retriever.invoke(query)
            context = "\n\n".join(d.page_content for d in docs)
            final_prompt = PROMPT.invoke({"context": context, "question": query})

        answer = st.write_stream(chunk.content for chunk in llm.stream(final_prompt))

        sources = [
            {
                "page": int(d.metadata.get("page", 0)) + 1,
                "text": d.page_content[:300] + "...",
            }
            for d in docs
        ]
        with st.expander("📚 Sources"):
            for s in sources:
                st.markdown(f"**Page {s['page']}**")
                st.caption(s["text"])

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )