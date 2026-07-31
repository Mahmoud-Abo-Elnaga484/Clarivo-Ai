# Clarivo-Ai
# Clarivo | AI Homework Companion

> **Informed pedagogy, operational clarity, and sustainable learning results.**
> Clarivo is a premium, AI-powered pedagogical assistant designed exclusively for parents. Instead of acting as a typical homework solver that bypasses the learning process, Clarivo analyzes assignments, cross-references them with official curriculum materials, and synthesizes a structured teaching framework. This empowers parents to guide, teach, and verify their child's understanding effectively.

---

## Key Features

*   **Intelligent Vision Extraction:** Capable of reading homework from both high-resolution images (JPG/PNG) and multi-page PDFs, accurately extracting subjects, topics, and specific questions.
*   **Curriculum Grounding (RAG Pipeline):** Allows parents to upload official textbooks or curriculum PDFs. The system indexes these documents to build teaching frameworks based strictly on approved materials, eliminating AI hallucinations.
*   **Smart Language Detection:** Automatically detects the language of the homework using advanced regex parsing, forcing the LLM to respond strictly in the appropriate language (e.g., Arabic or English).
*   **Premium Editorial UI/UX:** Built on Streamlit but completely re-skinned with custom CSS to deliver a dark, high-end, and minimalist user interface reminiscent of premium SaaS products.
*   **Self-Healing Data Parsing:** Features a robust fallback mechanism that automatically repairs malformed JSON outputs from the LLM, ensuring application stability without interrupting the user experience.

---

## System Architecture

Clarivo operates on a robust Retrieval-Augmented Generation (RAG) pipeline combined with advanced Computer Vision. 

1.  **Input Phase:** The user uploads a homework document and an optional textbook context.
2.  **Vision & OCR:** Google Gemini Flash processes the visual data, extracting the core questions and pedagogical context into a structured format.
3.  **Retrieval Phase:** The FAISS vector database performs a similarity search against the indexed curriculum to find the most relevant teaching methodologies.
4.  **AI Synthesis:** A large language model (e.g., Qwen) orchestrates the extracted questions and retrieved context to generate a parent-friendly teaching guide, common mistakes, and verified answers.
5.  **Rendering:** The frontend dynamically renders the synthesized plan into clean, readable cards.

---

## Project Structure

Clarivo/
|-- app.py                  # Streamlit UI & Core Application Loop
|-- vision.py               # Image Processing & Gemini Vision API Integration
|-- rag.py                  # Prompt Engineering & LLM Orchestration
|-- retriever.py            # FAISS Vector Database Management
|-- material_utils.py       # Text Extraction for Uploaded Curriculums
|-- pdf_utils.py            # PDF to Image Conversion Pipeline
|-- parser.py               # Pydantic Models for JSON Validation
|-- prompts.py              # LLM System Prompts and Rulesets
|-- requirements.txt        # Python Dependencies
|-- .env                    # Environment Secrets

---

## Installation & Setup

1.  **Clone the Repository:**
    git clone https://github.com/yourusername/clarivo.git
    cd clarivo

2.  **Create a Virtual Environment:**
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate

3.  **Install Dependencies:**
    pip install -r requirements.txt

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory and add your API keys:
    GOOGLE_API_KEY=your_api_key_here

---

## Running the Application

To start the Clarivo interface, execute the following command in your terminal:

```bash
streamlit run app.py
