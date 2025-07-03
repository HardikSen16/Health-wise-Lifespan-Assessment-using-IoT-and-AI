# Here are four objectives for the "Health-wise Lifespan Assessment using IoT and AI tools" project:
1. Data-Driven Health Monitoring and Analysis: Develop an integrated IoT system to monitor key health parameters such as physical activity, diet, sleep, and harmful habits, providing real-time insights into an individual’s health status.
2. Predictive Lifespan Assessment Using AI: Design and implement AI models to predict health risks and lifespan trends based on lifestyle habits, food intake, and sensor data, with the goal of promoting early intervention and healthier choices.
3. Personalized Health Recommendations: Build an AI-driven recommendation system that provides tailored lifestyle improvement suggestions (e.g., dietary adjustments, exercise routines) to enhance longevity and overall well-being.
4. Seamless User Engagement and Accessibility: Create a user-friendly application that integrates IoT-based data collection with AI analytics, enabling real-time access to health insights and fostering long-term user engagement through gamification and community benchmarking


# 🧠 Health-wise Lifespan Assessment using IoT and AI

This project integrates IoT-based real-time health monitoring with AI-powered lifespan prediction and personalized healthcare recommendations. It collects data using sensors connected to an ESP32 board, sends the data to Firebase, and uses a web interface powered by an XGBoost model and LLM chatbot for analysis and guidance.

---

## 📦 Project Folder Structure

```
Health-wise-Lifespan-Assessment-using-IoT-and-AI/
│
├── 📁 iot/
│   ├── iot_code.ino                   # ESP32 code for sensor data upload to Firebase
│   ├── README_IoT_Health_Monitoring.docx
│
├── 📁 ml_model/
│   ├── xgboost_model_code.ipynb       # XGBoost training pipeline
│   ├── life_expectancy_model.pkl      # Trained model
│   ├── README_XGBoost_LifeExpectancy_Model.docx
│
├── 📁 webpage_for_lifespan_and_chatbot/
│   ├── form_page.html
│   ├── prediction_chat.html
│   ├── scripts & stylesheets
│   ├── final_year_project_model.pkl
│   ├── README_Web_Lifespan_and_Chatbot.docx
│
├── 📁 knowledge_base/
│   ├── healthcare books (.pdf/.txt)
│   ├── making_pinecone_index_for_vectore_database_storage.ipynb
│   ├── README_Healthcare_KnowledgeBase_RAG.docx
│
├── 📄 README.md                       # Main guide (you are reading this)
```

---

## 🛠️ Components & Tools Used

### 🔧 Hardware
- ESP32 Dev Board
- MAX30100 or MAX30102 (Pulse & SpO2 Sensor)
- MLX90614 (Temperature Sensor)
- Breadboard, jumper wires, micro USB cable
- Wi-Fi enabled router

### 📦 Software
- Firebase Realtime Database
- Python, FastAPI, Scikit-learn, XGBoost
- LangChain, HuggingFace Transformers
- Pinecone (Vector DB)
- Arduino IDE

---

## 🔌 IoT Setup (ESP32 + Firebase)

### Circuit Diagram
📷 See `iot/README_IoT_Health_Monitoring.docx` or circuit image for wiring reference.

- MAX30100:
  - VIN → 3.3V
  - GND → GND
  - SDA → GPIO21
  - SCL → GPIO22
- MLX90614:
  - VIN → 3.3V
  - GND → GND
  - SDA → GPIO16
  - SCL → GPIO17

### Firebase Setup
1. Go to https://console.firebase.google.com/
2. Create a new project and enable **Realtime Database**
3. Set DB mode to **test** and copy your database URL
4. Replace placeholders in `iot_code.ino`
5. Flash the ESP32 via Arduino IDE

---

## 🌐 Web Interface

The `webpage_for_lifespan_and_chatbot/` folder contains:
- Form to collect age, gender, BMI, etc.
- JS fetches Firebase data (BPM, SpO2, Temperature) and fills the form
- Sends request to FastAPI backend
- Shows:
  - Predicted lifespan
  - Personalized recommendation
  - Chatbot for continuous interaction

### Tech Stack:
- HTML, JS, CSS (Frontend)
- FastAPI (Backend)
- LangChain + Mistral 7B + Pinecone (Chatbot)

---

## 🧠 AI Model: Life Expectancy Prediction

### XGBoost Model
- Trained on a **custom dataset** (see `ml_model/`)
- Features: Age, Gender, Diet, Exercise, Sleep, Medical History, BMI, etc.
- Used a pipeline with One-Hot Encoding + StandardScaler
- Achieved **R² Score of 0.89**
- Saved as `life_expectancy_model.pkl`

---

## 📚 Domain-Specific Knowledge Base (RAG)

- Healthcare books embedded using HuggingFace Transformers (MiniLM)
- Chunked (100–300 tokens)
- Stored in Pinecone DB
- Used for LLM-powered question answering

Download more books at: https://openstax.org/subjects/nursing

---

## 🧪 How to Run

1. Flash `iot_code.ino` to ESP32
2. Set up Firebase and confirm readings are live
3. Launch FastAPI backend:
```bash
uvicorn main:app --reload
```
4. Open `form_page.html` in browser
5. Fill or fetch health form, click Predict
6. Get predicted lifespan and start chatbot

---

## 📝 References

All references used to create the dataset and train the model are documented in:
- `README_Healthcare_KnowledgeBase_RAG.docx`
- `README_XGBoost_LifeExpectancy_Model.docx`
- `README_IoT_Health_Monitoring.docx`

---

## 🙌 Contributors

**Hardik Sen** – Developer & Researcher  
**Prof. Prashant M Prabhu, ECE department, MIT Manipal and	Dr. Spoorthi Singh, Mechatronics department, MIT Manipal** - Project guides
                                      

Project GitHub: [Health-wise-Lifespan-Assessment-using-IoT-and-AI](https://github.com/HardikSen16/Health-wise-Lifespan-Assessment-using-IoT-and-AI)



