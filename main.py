import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from requests.exceptions import RequestException


BASE_DIR = Path(__file__).resolve().parent
COLLECTION_NAME = "rag_collection"


def find_pdf(pdf_arg: str | None = None) -> Path:
    if pdf_arg:
        pdf_path = Path(pdf_arg)
        if not pdf_path.is_absolute():
            pdf_path = BASE_DIR / pdf_path
    else:
        candidates = [
            BASE_DIR / "document_loader" / "STATS.pdf",
            BASE_DIR / "Railway_Exam_Mathematics_120_Page_Practice_Book.pdf",
        ]
        pdf_path = next((path for path in candidates if path.is_file()), None)
        if pdf_path is None:
            pdf_path = next(iter(sorted(BASE_DIR.glob("*.pdf"))), None)

    if pdf_path is None or not pdf_path.is_file():
        raise FileNotFoundError(
            "No PDF found. Pass --pdf with the PDF path or place a PDF in the project directory."
        )
    return pdf_path


def build_rag(pdf_path: Path):
    api_key = os.getenv("NVIDIA_API_KEY") or os.getenv("NVDIA_API_KEY")
    if not api_key:
        raise RuntimeError(
            "NVIDIA API key is missing. Set NVIDIA_API_KEY in .env "
            "(or rename NVDIA_API_KEY to NVIDIA_API_KEY)."
        )

    print(f"Loading document from: {pdf_path}")
    docs = PyPDFLoader(str(pdf_path)).load()
    if not docs:
        raise ValueError(f"No readable content found in {pdf_path}")
    print(f"Loaded {len(docs)} document pages.")

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=80,
    ).split_documents(docs)
    if not chunks:
        raise ValueError("The PDF did not produce any text chunks.")
    print(f"Created {len(chunks)} text chunks.")

    embeddings = FastEmbedEmbeddings()
    client = QdrantClient(location=":memory:")
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    vectorstore = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )
    vectorstore.add_documents(chunks)
    print("Indexing complete.")

    llm = ChatNVIDIA(
        model="nvidia/nemotron-3.5-bolt-e4b",
        nvidia_api_key=api_key,
        temperature=0.2,
        max_completion_tokens=1024,
        timeout=60,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert tutor. Answer accurately using ONLY the provided "
                "context. If the answer is not in the context, say that you do not "
                "know.\n\nContext:\n{context}",
            ),
            ("human", "{question}"),
        ]
    )

    return vectorstore.as_retriever(search_kwargs={"k": 3}), prompt | llm | StrOutputParser()


def query_rag(question: str, retriever, rag_chain) -> str:
    question = question.strip()
    if not question:
        raise ValueError("Question cannot be empty.")

    retrieved_docs = retriever.invoke(question)
    print(f"\nRetrieved {len(retrieved_docs)} relevant context chunk(s):")
    for index, doc in enumerate(retrieved_docs, start=1):
        page_num = doc.metadata.get("page")
        page_label = int(page_num) + 1 if isinstance(page_num, int) else "Unknown"
        preview = doc.page_content.strip().replace("\n", " ")[:150]
        print(f" [{index}] (Page {page_label}): {preview}")

    context = "\n\n".join(doc.page_content for doc in retrieved_docs)
    print("\nGenerating response...")
    return rag_chain.invoke({"context": context, "question": question})


def main() -> int:
    load_dotenv(BASE_DIR / ".env")

    parser = argparse.ArgumentParser(description="Run a local PDF RAG assistant.")
    parser.add_argument("--pdf", help="Path to the PDF document")
    parser.add_argument("--question", help="Ask one question and exit")
    args = parser.parse_args()

    try:
        pdf_path = find_pdf(args.pdf)
        retriever, rag_chain = build_rag(pdf_path)

        if args.question:
            print("\nAnswer:")
            print(query_rag(args.question, retriever, rag_chain))
        else:
            print("\nRAG assistant ready. Enter 'exit' or 'quit' to stop.")
            while True:
                try:
                    question = input("\nQuestion: ").strip()
                except (EOFError, KeyboardInterrupt):
                    print()
                    break
                if question.lower() in {"exit", "quit"}:
                    break
                if not question:
                    continue
                print("\nAnswer:")
                print(query_rag(question, retriever, rag_chain))
        return 0
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"Error: {exc}")
        return 1
    except RequestException as exc:
        print(f"Error communicating with the NVIDIA API: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())





