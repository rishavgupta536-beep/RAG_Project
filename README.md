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
Create and activate a virtual environment:
python -m venv .venv
.venv\Scripts\activate

Install dependencies:
pip install -r requirement.txt

Configure environment variables:
Create a .env file in the root directory and add your API key:
API_KEY=your_api_key_here


# RAG Project — PDF Question & Answering System

A Python-based Retrieval-Augmented Generation (RAG) assistant that reads a PDF document (`Railway_Exam_Mathematics_120_Page_Practice_Book.pdf`), splits and indexes its content, and answers user queries directly from the retrieved context.

## Submitted By

* **Name:** Rishav Prakash Gupta
* **Roll No:** 202410101110244
* **Course:** B.Tech Computer Science and Engineering (3rd Year, Group 59, 50), Shri Ramswaroop Memorial University

## Features

* **PDF Knowledge Base:** Loads and processes a 120-page mathematics practice PDF (`Railway_Exam_Mathematics_120_Page_Practice_Book.pdf`).
* **Context-Grounded Answers:** Retrieves the top relevant chunks before generating an answer to avoid hallucinations.
* **Two Usage Modes:** Supports both interactive chat mode and single-question CLI execution.

## How to Run

1. **Install dependencies:**
   ```bash
   pip install -r requirement.txt
