# RAG Project – PDF Question & Answering System

A Python-based Retrieval-Augmented Generation (RAG) assistant that reads a PDF document (`Railway_Exam_Mathematics_120_Page_Practice_Book.pdf`), splits and indexes its content, and answers user queries directly from the retrieved context.

## Features
- **PDF Knowledge Base:** Loads and processes a 120-page mathematics practice PDF.
- **Context-Grounded Answers:** Retrieves the top relevant chunks before generating an answer to avoid hallucinations.
- **Two Usage Modes:** Supports both interactive chat mode and single-question CLI execution.

## Project Structure
- `main.py` — Core RAG pipeline, document retriever, and CLI interface.
- `Railway_Exam_Mathematics_120_Page_Practice_Book.pdf` — Source knowledge base PDF.
- `requirement.txt` — Python dependencies required to run the project.

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/rishavgupta536-beep/RAG_Project.git](https://github.com/rishavgupta536-beep/RAG_Project.git)
   cd RAG_Project
