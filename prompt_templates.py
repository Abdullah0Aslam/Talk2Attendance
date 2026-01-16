from langchain_core.prompts import ChatPromptTemplate

prompt1 = ChatPromptTemplate.from_messages([
    ("system", """Generate SQL query for this database:

{schema}

Return ONLY the SQL query, no explanation or markdown.

Examples:
- "How many users?" -> SELECT COUNT(*) FROM users
- "Show attendance" -> SELECT * FROM attendance"""),
    ("user", "{question}")
])



prompt2 = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant that converts database results into natural language.
Given a question and the database result, provide a clear, conversational answer.

Examples:
Question: "How many users?"
Result: "4"
Answer: "There are 4 users."

Question: "Who is on leave?"
Result: "Rahmat"
Answer: "Rahmat is on leave."

Question: "Show all users"
Result: "Ali, Hassan, Rahmat, Sara"
Answer: "Here are all the users: Ali, Hassan, Rahmat, and Sara."

Keep answers natural and conversational."""),
    ("user", """Question: {question}
Database Result: {result}

Provide a natural language answer:""")
])