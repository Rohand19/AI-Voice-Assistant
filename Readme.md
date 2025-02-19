# 🗣️ FastAPI Voice Assistant

A FastAPI-based voice assistant that processes user input, interacts with the Groq Cloud API for intent detection and responses, and logs interactions to a MongoDB database.

## 📋 Features

- 🧠 **Intent Detection**: Uses Groq Cloud API to understand user input and generate responses.
- 📊 **MongoDB Integration**: Stores user interactions for tracking and analysis.
- 🔥 **Async Support**: Fully asynchronous architecture using FastAPI and `httpx` for fast performance.
- 📡 **CORS Enabled**: Supports cross-origin requests for flexible integration with web clients.

---

## 📂 Project Structure

```
.
├── Dockerfile
├── .dockerignore
├── .env
├── main.py
├── requirements.txt
└── README.md
```

---

## 🛠️ Prerequisites

Ensure you have the following installed:

- [Python 3.11+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/)
- MongoDB (Local or Cloud instance)

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Rohand19/AI-Voice-Assistant
cd AI-Voice-Assistant
```

### 2️⃣ Set Up Environment Variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key_here
MONGODB_URI=mongodb://localhost:27017
```

### 3️⃣ Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 4️⃣ Run the FastAPI Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be live at: `http://localhost:8000`

---

## 🐳 Docker Instructions

### Build Docker Image

```bash
docker build -t fastapi-voice-assistant .
```

### Run Docker Container

```bash
docker run -p 8000:8000 --env-file .env fastapi-voice-assistant
```

Check if the API is live:

```bash
curl http://localhost:8000/docs
```

---

## 📊 API Endpoints

### ➤ `POST /process-voice`
Processes user input and returns an appropriate response.

**Request:**
```json
{
  "text": "What is the weather today?",
  "user_id": "123"
}
```

**Response:**
```json
{
  "response": "Today's weather is sunny with a high of 25°C."
}
```

### ➤ `GET /docs`
Interactive API documentation (Swagger UI).

---

## 📋 Logs and Database
- User inputs and responses are logged in MongoDB under the `voice_assistant.interactions` collection.

---

## 🧹 Cleanup and Stop Containers

```bash
docker ps  # Find the container ID
docker stop <container_id>
docker system prune -f  # Clean up unused images and containers
```

---

## 🛠️ Troubleshooting

1. **Invalid API Key**: Ensure `GROQ_API_KEY` is valid and active.
2. **MongoDB Connection**: Verify MongoDB is running and the URI is correct.
3. **Docker Build Issues**: Clear Docker cache with `docker system prune -f` and rebuild.

---

## 📌 Future Enhancements

- ✅ Add user authentication.
- ✅ Implement speech-to-text support.
- ✅ Improve response accuracy with fine-tuned models.

---

## 📜 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Commit changes: `git commit -m "Add your feature"`.
4. Push to the branch: `git push origin feature/your-feature`.
5. Submit a pull request.

---

## ⭐ Acknowledgments

Thanks to [Groq](https://www.groq.com/) for providing the API service.

---

## 📧 Contact

For questions or support, reach out at: `rohanb2000@gmail.com`.

