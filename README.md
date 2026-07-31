# Clarivo | AI Homework Companion

> **Informed pedagogy, operational clarity, and sustainable learning results.**
> Clarivo is a premium, AI-powered pedagogical assistant designed exclusively for parents. Instead of acting as a typical homework solver that bypasses the learning process, Clarivo analyzes assignments, cross-references them with official curriculum materials, and synthesizes a structured teaching framework. This empowers parents to guide, teach, and verify their child's understanding effectively.

---

## Key Features

*   **Intelligent Vision Extraction:** Capable of reading homework from both high-resolution images (JPG/PNG) and multi-page PDFs, accurately extracting subjects, topics, and specific questions.
*   **Curriculum Grounding (RAG Pipeline):** Allows parents to upload official textbooks or curriculum PDFs. The system indexes these documents to build teaching frameworks based strictly on approved materials, eliminating AI hallucinations.
*   **Smart Language Detection:** Automatically detects the language of the homework using advanced regex parsing, forcing the LLM to respond strictly in the appropriate language (e.g., Arabic or English).
*   **Decoupled GPU Architecture (Kaggle & ngrok):** Utilizes a remote Qwen LLM hosted on Kaggle GPUs, tunneled seamlessly to the local frontend via ngrok for high-performance inference without requiring expensive local hardware.
*   **Premium Editorial UI/UX:** Built on Streamlit but completely re-skinned with custom CSS to deliver a dark, high-end, and minimalist user interface reminiscent of premium SaaS products.
*   **Self-Healing Data Parsing:** Features a robust fallback mechanism that automatically repairs malformed JSON outputs from the LLM, ensuring application stability without interrupting the user experience.

---

## System Architecture

Clarivo operates on a robust Retrieval-Augmented Generation (RAG) pipeline combined with advanced Computer Vision, utilizing a distributed architecture for heavy LLM processing.

1.  **Input Phase:** The user uploads a homework document and an optional textbook context via the local Streamlit interface.
2.  **Vision & OCR:** Google Gemini Flash processes the visual data, extracting the core questions and pedagogical context into a structured format.
3.  **Retrieval Phase:** The FAISS vector database performs a similarity search against the local curriculum index to find the most relevant teaching methodologies.
4.  **AI Synthesis (Kaggle Engine):** The extracted data and retrieved context are sent via an `ngrok` tunnel to a remote Kaggle instance running a powerful open-source LLM (Qwen). The model generates a parent-friendly teaching guide, common mistakes, and verified answers.
5.  **Rendering:** The frontend dynamically receives the structured JSON response and renders the synthesized plan into clean, readable UI cards.

---

## Project Structure

Clarivo/
|-- app.py                  # Streamlit UI & Core Application Loop
|-- vision.py               # Image Processing & Gemini Vision API Integration
|-- rag.py                  # API routing to the Kaggle-hosted Qwen model
|-- retriever.py            # FAISS Vector Database Management
|-- material_utils.py       # Text Extraction for Uploaded Curriculums
|-- pdf_utils.py            # PDF to Image Conversion Pipeline
|-- parser.py               # Pydantic Models for JSON Validation
|-- prompts.py              # LLM System Prompts and Rulesets
|-- requirements.txt        # Python Dependencies
|-- .env                    # Environment Secrets (API Keys & ngrok URL)

---

## Installation & Setup

Because Clarivo relies on a heavy language model (Qwen), the system architecture is split into two parts: hosting the backend model on Kaggle and running the frontend locally.

### Part 1: Backend Setup (Kaggle & ngrok)
1.  Open your Kaggle notebook containing the Qwen model and FastAPI setup.
2.  Start the FastAPI server within the notebook to serve the model.
3.  Initialize `ngrok` within the notebook to expose the local Kaggle server to the public internet.
4.  Copy the generated forwarding URL (e.g., `https://<random-id>.ngrok-free.app`).

### Part 2: Frontend Setup (Local Machine)
1.  **Clone the Repository:**
    git clone [https://github.com/yourusername/clarivo.git](https://github.com/Mahmoud-Abo-Elnaga484/Clarivo-Ai)
    cd clarivo

2.  **Create a Virtual Environment:**
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate

3.  **Install Dependencies:**
    pip install -r requirements.txt

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory. Add your Google Vision API key and the ngrok URL generated from your Kaggle notebook:
    GOOGLE_API_KEY=your_google_api_key_here
    NGROK_URL=https://<your-ngrok-id>.ngrok-free.app

---

## Running the Application

Once the Kaggle backend is running and the `.env` file is properly configured with the active ngrok URL, start the Clarivo interface by executing the following command in your local terminal:

```bash
streamlit run app.py
