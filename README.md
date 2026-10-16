<div align="center">

# 📄💬 Chat with your PDF

### Drop in a document. Ask it anything. Get answers with receipts.

*A Retrieval-Augmented Generation (RAG) app that turns any PDF into a conversation.*

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/Framework-LangChain-1C3C3C)
![ChromaDB](https://img.shields.io/badge/Vector%20DB-Chroma-FF6F00)
![OpenAI](https://img.shields.io/badge/LLM-OpenAI-412991?logo=openai&logoColor=white)

---

## ✨ What is this?

Ever opened a 200-page PDF and thought *"I just need one answer from this"*?

This app lets you **upload your own PDF** and **chat with it**. It reads the document, understands it, and answers your questions using **only what's actually in the file**. If the answer isn't there, it says **"I don't know"** instead of making something up.

No hallucinated facts. No endless scrolling. Just answers, and the exact pages they came from.

---

## 🎬 How it works

```
   📄 Your PDF
        │
        ▼
   ✂️  Split into overlapping chunks (1000 chars, 200 overlap)
        │
        ▼
   🧠 Embed each chunk  (text-embedding-3-large)
        │
        ▼
   🗄️  Store in Chroma (in-memory, private to your session)
        │
        │            ❓ Your question
        │                   │
        ▼                   ▼
   🔍 MMR Retriever finds the 4 most relevant, least repetitive chunks
        │
        ▼
   🤖 GPT-4 reads those chunks + your question
        │
        ▼
   💬 Streaming answer + 📚 source pages
```

**Why MMR?** Maximal Marginal Relevance fetches 10 candidates and keeps the 4 that are both relevant *and* different from each other, so you get varied context instead of the same paragraph four times.

---

## 🚀 Features

| | Feature | Details |
|---|---|---|
| 📤 | **Bring your own PDF** | Upload any PDF straight from the sidebar |
| 💬 | **Chat interface** | Full conversation history, just like a messaging app |
| ⚡ | **Streaming answers** | Responses appear word by word as they're generated |
| 📚 | **Source citations** | Every answer shows the pages and snippets it used |
| 🔒 | **Session-private** | Each upload gets its own in-memory store, so documents never mix |
| 🧹 | **One-click reset** | Clear the chat, or upload a new PDF for a fresh start |
| 🛡️ | **Honest by design** | Says "I don't know" when the context doesn't have the answer |

---

## 🛠️ Getting started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd rag-app
```

### 2. Create a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your OpenAI API key

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-your-key-here
```

> ⚠️ **Never commit your `.env` file.** Make sure it's listed in `.gitignore`.

### 5. Launch the app

```bash
streamlit run app.py
```

Open **http://localhost:8501**, upload a PDF, and start asking questions. 🎉

---

## 💡 Try asking

Once your PDF is loaded, try questions like:

- *"Summarize the main idea of chapter 2."*
- *"What does the document say about backpropagation?"*
- *"List the key terms defined in this paper."*
- *"What are the limitations mentioned by the authors?"*
- *"What is the capital of Mars?"* → *(watch it honestly say "I don't know" 😉)*

---

## 🧰 Tech stack

| Layer | Tool |
|---|---|
| **UI** | [Streamlit](https://streamlit.io/) |
| **Orchestration** | [LangChain](https://www.langchain.com/) |
| **PDF parsing** | PyPDF |
| **Text splitting** | `RecursiveCharacterTextSplitter` |
| **Embeddings** | OpenAI `text-embedding-3-large` |
| **Vector store** | [ChromaDB](https://www.trychroma.com/) |
| **LLM** | OpenAI `gpt-4-0613` |

---

## ⚙️ Configuration

Want to tweak the behavior? Everything lives in `app.py`:

| Setting | Where | Default |
|---|---|---|
| Chunk size | `RecursiveCharacterTextSplitter` | `1000` |
| Chunk overlap | `RecursiveCharacterTextSplitter` | `200` |
| Chunks sent to the LLM (`k`) | `search_kwargs` | `4` |
| Candidates considered (`fetch_k`) | `search_kwargs` | `10` |
| Relevance vs. diversity (`lambda_mult`) | `search_kwargs` | `0.5` |
| Max upload size | `.streamlit/config.toml` | `50 MB` |

---

## 🧭 Known limitations

- 🖼️ **Scanned PDFs** (images of text) won't work without OCR, since the parser reads selectable text only.
- 💾 **In-memory storage:** restarting the server clears uploaded documents.
- 📄 **One PDF at a time** per session.

---

## 🔮 Roadmap

- [ ] Multi-PDF chat
- [ ] Conversation memory for follow-up questions
- [ ] OCR support for scanned documents
- [ ] Persistent per-user document libraries
- [ ] Support for `.docx` and `.txt` files
- [ ] Docker setup and cloud deployment

---

## 🤝 Contributing

Ideas and improvements are welcome!

1. Fork the repo
2. Create your branch: `git checkout -b feature/cool-idea`
3. Commit your changes: `git commit -m "Add cool idea"`
4. Push: `git push origin feature/cool-idea`
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.

---

<div align="center">

**Built with ☕, curiosity, and a lot of `pip install` by Hasnain**

*Started as a RAG learning project. Grew into something people can actually use.*

⭐ If this helped you, consider giving the repo a star!

</div>
