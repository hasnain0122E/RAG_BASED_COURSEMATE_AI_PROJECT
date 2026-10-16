from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter

data = PyPDFLoader("./document_loader/GRU.pdf")
splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=10)

Docs = data.load()
chunks = splitter.split_documents(Docs)

print(chunks[0].page_content)
