# 🚀 DocuChat - AI-Powered Multilingual Document Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)

DocuChat is an intelligent document assistant powered by RAG (Retrieval-Augmented Generation) that transforms your documents into an interactive, multilingual AI chatbot.

## ✨ Features

### 🌍 Multilingual Support
- **Interface**: English, Français, العربية
- **Chat**: Understands and responds in ANY language
- **RTL Support**: Automatic right-to-left for Arabic

### 📚 Smart Document Processing
- **Multi-format Upload**: PDF, TXT, DOCX
- **Drag & Drop**: Intuitive file upload
- **Auto-indexing**: Embedding-based vector search
- **Multi-document Synthesis**: Intelligent cross-document analysis

### 🔐 Secure Authentication
- **JWT**: Token-based authentication
- **OAuth**: Google login integration
- **Visual Captcha**: Anti-bot protection
- **User Isolation**: Documents separated per user

### 💬 Intelligent Chat
- **Context-aware**: Answers based on YOUR documents
- **Source Citation**: Automatic source references
- **Multi-doc Queries**: Synthesizes information across all documents
- **Conversation History**: Save, export, and manage chats

### 🎨 Modern Interface
- **Light/Dark Mode**: Toggle between themes
- **Responsive Design**: Works on all devices
- **Clean UI**: Professional design
- **Real-time Updates**: Instant responses

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Groq API Key ([Get one free](https://console.groq.com/))

### Installation

```bash
# Clone repository
git clone https://github.com/[your-username]/docuchat.git
cd docuchat

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add GROQ_API_KEY

# Frontend
cd ../frontend
npm install

# Run (2 terminals)
# Terminal 1:
cd backend && python -m uvicorn main:app --reload --port 8000

# Terminal 2:
cd frontend && npm start
```

Access: http://localhost:3000

## 🛠️ Technology Stack

**Backend**: FastAPI, Groq (LLama 3.3 70B), Sentence Transformers
**Frontend**: React 18, Custom CSS
**Auth**: JWT + OAuth 2.0
**RAG**: Custom vector index with embeddings

## 📖 Usage Examples

```
English: "Summarize all documents"
Français: "Quel est le budget total?"
العربية: "ما هي النقاط الرئيسية؟"
```

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 🙏 Acknowledgments

- [Groq](https://groq.com/) - LLM API
- [FastAPI](https://fastapi.tiangolo.com/) - Backend
- [React](https://reactjs.org/) - Frontend

---

**Made with ❤️ and AI**
