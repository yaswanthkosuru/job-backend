from langchain_core.prompts import ChatPromptTemplate

summary_template = ChatPromptTemplate.from_messages([
    ("system", 
     "Summarize the following text in one clear and concise paragraph, capturing the key ideas without missing critical points. Ensure the summary is easy to understand and avoids excessive detail"
     ),
    ("human", "{input}")
])
