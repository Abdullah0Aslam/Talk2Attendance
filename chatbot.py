from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from database import engine
from prompt_templates import prompt1, prompt2
from dotenv import load_dotenv
import os
load_dotenv()

db = SQLDatabase(engine, include_tables=["users", "attendance"])

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0
)

def ask_database(question):
    
    schema = db.get_table_info()
    response = llm.invoke(prompt1.format(schema=schema, question=question))
    sql = response.content.strip().replace("```sql", "").replace("```", "").strip().rstrip(";")
    # print(sql)
    result = db.run(sql)
    natural_response = llm.invoke(prompt2.format(question=question,result=result))
    return natural_response.content.strip()


print("Type 'exit' to quit\n")
while True:
    question = input("You: ").strip()
    if question.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break
    print(f"Bot: {ask_database(question)}\n")