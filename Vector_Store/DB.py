from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma
from dotenv import load_dotenv
load_dotenv()


docs = [
    Document(
        page_content=(
        "Authentication is handled via OAuth 2.0. "
        "Developers must pass a Bearer token in the Authorization header "
        "for all API requests. Tokens expire after 3,600 seconds."
        ),
        metadata={
        "source": "api-docs-v2",
        "category": "security",
        "version": "2.4",
        "access_level": "internal",
        "author": "DevOps Team",
        },
    ),
    Document(
        page_content=(
        "To reset your forgotten password, click on the 'Forgot Password' link "
        "on the login screen. Enter your registered email address to receive "
        "a secure reset link valid for 30 minutes."
        ),
        metadata={
        "source": "help_center_faq",
        "category": "account_management",
        "platform": "cross-platform",
        "doc_id": "FAQ-1092",
        "last_updated": "2026-03-15",
        },
    ),
    Document(
        page_content=(
        "Transformer-based architectures rely heavily on self-attention mechanisms "
        "to process sequential input data simultaneously, bypassing the recurrence "
        "limitations found in traditional recurrent neural networks (RNNs)."
        ),
        metadata={
        "source": "arXiv:1706.03762",
        "category": "machine_learning",
        "publication_year": 2017,
        "peer_reviewed": True,
        "tags": ["nlp", "transformers", "deep_learning"],
        },
    )
]

embedding_model = OpenAIEmbeddings(model = "text-embedding-3-large" )

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    persist_directory="chroma_db"
)

results = vectorstore.similarity_search("what are security best practices?", k = 2)

for r in results:
    print(r.page_content)
    print(r.metadata)
