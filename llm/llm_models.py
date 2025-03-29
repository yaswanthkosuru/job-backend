from langchain_groq import ChatGroq

import os

os.environ["GROQ_API_KEY"] = (
    "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"  # Use your actual Groq API key
)

groq_lama_model = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
)
