<<<<<<< HEAD
# eep-genai-2505
=======
# 🏆 Talent Matching Bot - Backend

The **Talent Matching Bot** backend is a **FastAPI-powered service** that enables AI-driven candidate matching for **Client Service Teams (CSTs)**. It integrates with **OpenAI's API** to rank candidates based on job requirements and predefined candidate data.

---

## 📌 Features

✅ **FastAPI-based backend** – Lightweight and efficient API for handling talent matching requests  
✅ **AI-powered matching** – Uses **OpenAI's LLM** to evaluate and rank candidates  
✅ **Predefined candidate database** – Loads candidates from a JSON file to simulate a real database  
✅ **CORS enabled** – Supports frontend requests from React/[Streamlit](https://streamlit.io/)\
✅ **Automatic ranking** – Returns top **3 best-fit candidates** based on job criteria

---

## 🛠️ Tech Stack

| **Technology**   | **Usage**                        |
| ---------------- | -------------------------------- |
| FastAPI (Python) | Backend API                      |
| OpenAI API       | AI-powered candidate ranking     |
| Uvicorn          | ASGI server for running FastAPI  |
| JSON Server      | Mock database for authentication |
| Python dotenv    | Environment variable management  |

---

## 🚀 Getting Started

### **🔹 Prerequisites**

Make sure you have the following installed:

- **Python** (v3.9+)
- **pip** (latest version)
- **OpenAI API Key** (LLM integration)
- [**Postman**](https://mckinsey.service-now.com/ghd?id=mck_app_cat_item&utm_medium=web&utm_source=ghd_website&utm_content=ai_search_result&table=pc_software_cat_item&sys_id=4a2237eb1bbf71d4d345eb91604bcb97&searchTerm=Postman) (Interacting with API)

---

### **🔹 Backend Setup (FastAPI)**

1️⃣ **Clone the repository**

```bash
git clone https://github.com/your-repo/talent-matching-bot.git
cd talent-matching-bot/backend
```

2️⃣ **Create a virtual environment and install dependencies**

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

3️⃣ **Set up OpenAI API Key by createing a .env file at the root level and adding:**

```bash
OPENAI_API_KEY=your-openai-api-key-here
```

4️⃣ **Start the backend server**

```bash
uvicorn app.main:app --reload
```

- The backend runs on http://127.0.0.1:8000

5️⃣ **Test route with Postman**

Open your Postman client and execute a GET request to http://127.0.0.1:8000.

You should receive the following response:

```json
{ "message": "Talent Matching Bot Backend is running!" }
```

---

## 📌 API Endpoints

- POST (/match) - Submits job details and retrieves top 3 matched candidates
- GET (/) - health check route

---

## 📜 License

## This project is licensed under the MIT License.
>>>>>>> 338bc9e (Initial commit)
