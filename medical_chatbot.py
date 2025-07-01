import os
from dotenv import load_dotenv, find_dotenv
from huggingface_hub import InferenceClient
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.llms.base import LLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from typing import Optional, List, Any
from pydantic import Field

# 🔹 Load environment variables
load_dotenv(find_dotenv())
HF_TOKEN = os.getenv("HF_TOKEN")
HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"
INDEX_NAME = "medicalbot"

# 🔹 Custom ChatCompletion LLM
class ChatCompletionLLM(LLM):
    repo_id: str
    token: str
    temperature: float = 0.5
    max_tokens: int = 1024
    client: Any = Field(default=None, exclude=True)

    class Config:
        extra = "allow"

    def __init__(self, **data):
        super().__init__(**data)
        self.client = InferenceClient(model=self.repo_id, token=self.token)

    @property
    def _llm_type(self) -> str:
        return "hf_chat_completion"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful medical assistant. Only use trusted sources and context provided."},
            {"role": "user", "content": prompt}
        ]
        response = self.client.chat_completion(
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message["content"].strip()

# 🔹 Load LLM
def load_llm(repo_id):
    return ChatCompletionLLM(repo_id=repo_id, token=HF_TOKEN)

# 🔹 Prompt Template
CUSTOM_PROMPT_TEMPLATE = """
Use the information provided in the context to answer the user's question.
If you don't know the answer, say you don't know. Do not guess or fabricate answers.

Context: {context}
Question: {question}

Answer:
"""

def set_custom_prompt(template):
    return PromptTemplate(template=template, input_variables=["context", "question"])

# 🔹 Load Embeddings
def download_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        encode_kwargs={"batch_size": 32}
    )

# 🔹 Pinecone setup
embeddings = download_embeddings()
docsearch = PineconeVectorStore.from_existing_index(index_name=INDEX_NAME, embedding=embeddings)
retriever = docsearch.as_retriever(search_kwargs={'k': 3})

# 🔹 Memory for chat history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 🔹 Create the QA Chain with chat memory
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=load_llm(HUGGINGFACE_REPO_ID),
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs={'prompt': set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)}
)

# 🔹 Generate Recommendations and Store in Memory
def generate_llm_recommendations(user_data):
    prompt = f"""You are a health assistant AI. Based on the user profile below, generate detailed and personalized health and lifestyle recommendations.

Always include analysis and advice regarding:
- **Heart Rate (bpm)** — Explain if it's low, normal, or high based on age/gender, and suggest improvements or actions.
- **SpO2 Level (%)** — Indicate whether the oxygen saturation is healthy or concerning, and provide breathing/lifestyle suggestions.
- **Body Temperature (°C)** — This reading is in Celsius. Analyze whether it's normal, low, or high, and offer potential causes and advice.

Also, provide well-rounded recommendations for improving health, habits, and preventing lifestyle-related diseases using the rest of the user profile.

User Data:
Age: {user_data['age']}
Gender: {user_data['gender']}
Country: {user_data['country']}
Exercise hours/week: {user_data['exercise']}
Diet: {user_data['diet']}
Medical History: {user_data['medical']}
Work Stress Level: {user_data['stress']}
Smoking: {user_data['smoking']}
Alcohol Consumption: {user_data['alcohol']}
Social Life: {user_data['social']}
BMI: {user_data['bmi']}
Sleep hours/day: {user_data['sleep']}
Heart Rate (bpm): {user_data['heartRate']}
SpO2 Level (%): {user_data['spo2']}
Body Temperature (°C): {user_data['temperature']}

Start with recommendations based on the three vital signs (Heart Rate, SpO2, Body Temperature), then continue with broader health and lifestyle advice."""

    try:
        result = qa_chain.invoke({"question": prompt})
        answer = result.get("answer", "").strip()

        if not answer:
            raise ValueError("Received empty recommendation from LLM.")

        memory.chat_memory.add_user_message(prompt)
        memory.chat_memory.add_ai_message(answer)
        return answer

    except Exception as e:
        print("Error generating LLM recommendations:", e)
        return "Sorry, we couldn't generate a personalized recommendation at this moment. Please try again later."

# 🔹 Expose qa_chain for live chat
def chat_with_bot(user_input: str) -> str:
    try:
        print("🧠 User Input to LLM:", user_input)
        result = qa_chain.invoke({"question": user_input})
        print("✅ LLM Response:", result)

        memory.chat_memory.add_user_message(user_input)
        memory.chat_memory.add_ai_message(result["answer"])

        return result["answer"]
    except Exception as e:
        print("❌ Error in chat_with_bot:", e)
        return "Sorry, I couldn't understand that."


    # Make sure you have a conversation chain set up (retriever + memory)
    #result = qa_chain({"question": user_input})
    #return result["answer"]

