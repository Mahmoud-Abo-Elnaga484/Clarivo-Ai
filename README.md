# 🚀 [Tips Hindawi](https://www.tipshindawi.com/) Challenge (June–July) 2026

> 🏆 This repository is my official submission for the [ **Tips Hindawi** ](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

## 👤 Participant

| Field            | Value                                |
| ---------------- | ------------------------------------ |
| Full Name        | Mahmoud Ashraf Abo-Elnaga            |
| Project Name     | Clarivo \| AI Homework Companion     |
| GitHub Username  | [Mahmoud-Abo-Elnaga484]               |
| Challenge Batch  | June–July 2026                       |
| Training Program | Large Language Models (LLMs) Program |
| Organization     | [**Edrak for Ai**](https://edrak4ai.com/en) |

---

# 📖 Project Overview

**Clarivo** is a premium, AI-powered pedagogical assistant designed exclusively for parents. Instead of acting as a typical homework solver that bypasses the learning process, Clarivo analyzes assignments, cross-references them with official curriculum materials, and synthesizes a structured teaching framework. This empowers parents to guide, teach, and verify their child's understanding effectively with informed pedagogy, operational clarity, and sustainable learning results.

---

# ✨ Features

* **Intelligent Vision Extraction:** Capable of reading homework from both high-resolution images (JPG/PNG) and multi-page PDFs, accurately extracting subjects, topics, and specific questions.
* **Curriculum Grounding (RAG Pipeline):** Allows parents to upload official textbooks or curriculum PDFs. The system indexes these documents to build teaching frameworks based strictly on approved materials, eliminating AI hallucinations.
* **Smart Language Detection:** Automatically detects the language of the homework using advanced regex parsing, forcing the LLM to respond strictly in the appropriate language (e.g., Arabic or English).
* **Decoupled GPU Architecture (Kaggle & ngrok):** Utilizes a remote Qwen LLM hosted on Kaggle GPUs, tunneled seamlessly to the local frontend via ngrok for high-performance inference without requiring expensive local hardware.
* **Premium Editorial UI/UX:** Built on Streamlit but completely re-skinned with custom CSS to deliver a dark, high-end, and minimalist user interface reminiscent of premium SaaS products.
* **Self-Healing Data Parsing:** Features a robust fallback mechanism that automatically repairs malformed JSON outputs from the LLM, ensuring application stability without interrupting the user experience.

---

# 🛠️ Technologies Used

* **Frontend & UI:** Streamlit, Custom CSS
* **AI & Vision Model:** Google Gemini Flash, Qwen LLM
* **RAG Pipeline:** FAISS (Vector Database)
* **Backend & Routing:** FastAPI, Pydantic (JSON Validation)
* **Infrastructure:** Kaggle GPUs, ngrok (Tunneling)
* **Language:** Python

---

# ⚙️ Installation

Because Clarivo relies on a heavy language model (Qwen), the system architecture is split into two parts: hosting the backend model on Kaggle and running the frontend locally.

### Part 1: Backend Setup (Kaggle & ngrok)
1. Open your Kaggle notebook containing the Qwen model and FastAPI setup.
2. Start the FastAPI server within the notebook to serve the model.
3. Initialize ngrok within the notebook to expose the local Kaggle server to the public internet.
4. Copy the generated forwarding URL (e.g., `https://<random-id>.ngrok-free.app`).

### Part 2: Frontend Setup (Local Machine)
1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/yourusername/clarivo.git](https://github.com/yourusername/clarivo.git) 
   cd clarivo
   ```
2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv 
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Environment Variables:**
   Create a `.env` file in the root directory. Add your Google Vision API key and the ngrok URL generated from your Kaggle notebook:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here 
   NGROK_URL=https://<random-id>.ngrok-free.app
   ```

---

# 🚀 Usage

Once the Kaggle backend is running and the `.env` file is properly configured with the active ngrok URL, start the Clarivo interface by executing the following command in your local terminal:

```bash
streamlit run app.py
```
* **Step 1:** Upload a homework document (image or PDF) via the local Streamlit interface.
* **Step 2:** (Optional) Upload official textbook context for curriculum grounding.
* **Step 3:** The system will dynamically receive the structured JSON response and render the synthesized teaching plan into clean, readable UI cards.

---

# 📸 Demo
 <img width="1527" height="692" alt="Screenshot 2026-07-31 155802" src="https://github.com/user-attachments/assets/e408a1f9-4200-4b07-9114-beac25ecda35" />
<img width="1535" height="692" alt="Screenshot 2026-07-31 155856" src="https://github.com/user-attachments/assets/0e9ca708-6bc1-478f-b7c7-5d4b955cd47b" />

<img width="1535" height="725" alt="Screenshot 2026-07-31 155935" src="https://github.com/user-attachments/assets/2c9450bc-bd40-4403-a146-666d8fba26e1" />


---

# 📈 Results

Clarivo successfully implements a distributed Retrieval-Augmented Generation (RAG) architecture, bridging advanced Computer Vision via Gemini Flash with a heavy Qwen LLM backend. The result is a highly performant, self-healing pedagogical assistant that seamlessly processes complex visual data into structured, parent-friendly teaching guides without requiring costly local hardware setups. 

---

# 🔮 Future Improvements

* Integrate an automated grading feature based on uploaded curriculum rubrics.
* Expand the smart language detection to support and output in additional global languages.
* Develop a persistent user profile system to track a child's learning progress and weak points over time.

---

# 📚 About the Challenge

This project was developed as part of the [**Tips Hindawi**](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

[Tips Hindawi](https://www.tipshindawi.com/) is the internships department of [**Edrak for Ai**](https://edrak4ai.com/en), and the challenge encourages participants to build real-world projects, apply practical skills, and showcase their work through GitHub.

For more information about the challenge, training programs, and upcoming batches, visit the official [Tips Hindawi](https://www.tipshindawi.com/) website.

---

# 📄 License

This project is shared for educational and portfolio purposes.
