# 🧠 Prompt & Experiment Tracker

> A Flask + Streamlit web app for organizing prompts, logging model experiments, and discovering which prompt–model combinations work best in your daily AI workflow.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-Backend-black.svg)](https://flask.palletsprojects.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-ff4b4b.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)](https://github.com/yourusername/prompt-experiment-tracker/graphs/commit-activity)

---

## 📋 Table of Contents

- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 The Problem

Working with LLMs in real projects quickly becomes messy:

- 🧾 **Prompt Sprawl** – Dozens of prompts scattered across chats, notebooks, and files  
- 🎲 **Untracked Experiments** – You tweak models/temperatures but never log what actually worked  
- 🧠 **No Memory** – Great prompts get lost in history instead of becoming reusable building blocks  
- 📉 **No Evidence** – It’s hard to say which prompt–model combo is objectively better  

**Result**: Repeating the same experiments and reinventing prompts every week.

---

## ✨ The Solution

**Prompt & Experiment Tracker** turns prompt hacking into a structured workflow:

git clone https://github.com/yourusername/prompt-experiment-tracker.git
cd prompt-experiment-tracker


2. **Create and activate a virtual environment (optional)**

python -m venv .venv
source .venv/bin/activate # macOS / Linux

.venv\Scripts\activate # Windows


3. **Install dependencies**

pip install -r requirements.txt


---

## 💻 Usage

### 1. Start the Flask backend

cd backend
python app.py


Backend runs at:

http://localhost:5001


### 2. Start the Streamlit frontend

Open a new terminal:

cd frontend
streamlit run dashboard.py


Frontend runs at:

http://localhost:8501


Make sure `API_BASE` in `frontend/dashboard.py` matches the backend URL:

API_BASE = "http://localhost:5001"


---

## 🧭 Project Structure

prompt-experiment-tracker/
│
├── backend/
│ ├── app.py # Flask API (prompts & experiments)
│ └── db.py # SQLAlchemy models & DB initialization
│
├── frontend/
│ └── dashboard.py # Streamlit UI (Prompts, Experiments, Analytics)
│
├── requirements.txt # Python dependencies
└── README.md # This file


---

## ⚙️ Configuration

You can tweak basic settings:

- Change backend port in `backend/app.py`:

app.run(host="0.0.0.0", port=5001, debug=True)


- Point Streamlit to a different URL in `frontend/dashboard.py`:

API_BASE = "http://localhost:5001"


- Swap SQLite for another database by updating the URL in `backend/db.py`:

DB_URL = "sqlite:///prompts.db"

e.g. postgresql://user:password@localhost/dbname


---

## 🗺️ Roadmap

Planned / nice-to-have improvements:

- [ ] User accounts / multi-tenant support  
- [ ] Export & import prompts/experiments (CSV / JSON)  
- [ ] Direct LLM API integration to run experiments from the UI  
- [ ] Tag-based analytics and filters (e.g. only “summarization” prompts)  
- [ ] Dark mode and UI polish  

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo  
2. Create a feature branch: `git checkout -b feature/my-feature`  
3. Commit your changes: `git commit -m "Add my-feature"`  
4. Push the branch: `git push origin feature/my-feature`  
5. Open a Pull Request  

Ideas:

- Better analytics & visualizations  
- Integration with OpenAI/Anthropic/etc. APIs  
- Export to markdown or Notion  
- Advanced search over prompts and notes  

---

<div align="center">

**Built with ❤️ for the AI community — so great prompts never get lost again.**

</div>
