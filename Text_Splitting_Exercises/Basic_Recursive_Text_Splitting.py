from langchain_text_splitters import RecursiveCharacterTextSplitter

article = """Artificial Intelligence (AI) has rapidly transitioned from science fiction into a defining cornerstone of modern technology. By enabling machines to learn from data, reason, and adapt, AI is reshaping industries, redefining human capability, and challenging our understanding of what technology can achieve. At its core, AI encompasses various subfields, including machine learning and deep learning. These systems process vast datasets at unprecedented speeds, recognizing complex patterns that human minds might miss. Today, AI powers diverse applications, from healthcare diagnostics and personalized education to autonomous transportation and climate modeling. In medicine, algorithms analyze medical imaging with remarkable precision, helping doctors detect diseases like cancer earlier than ever before. Meanwhile, businesses leverage AI-driven analytics to optimize supply chains, predict consumer trends, and enhance operational efficiency. However, this technological revolution brings significant challenges. The rapid deployment of AI raises pressing ethical questions regarding data privacy, algorithmic bias, and workforce displacement. As automation replaces routine tasks, concerns grow about economic inequality and the future of employment. Furthermore, ensuring that AI systems remain transparent, fair, and accountable is a critical priority for policymakers and developers alike. Ultimately, artificial intelligence is a powerful tool—an amplifier of human ingenuity. Its long-term impact will not be determined by the technology itself, but by the choices we make today. By establishing robust ethical frameworks, fostering inclusive innovation, and prioritizing human-centric values, we can harness AI to solve global challenges and build a more prosperous, equitable future for all."""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300, chunk_overlap=50
)

chunks = splitter.split_text(article)

print('TOTAL CHUNKS:', len(chunks))

for i, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {i} ---")
    print("Character count:", len(chunk))
    print(chunk)