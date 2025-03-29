from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

groq_lama_model = ChatGroq("llama-3.3-70b-versatile", api_key="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")