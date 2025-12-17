import ollama

def ask_llm(prompt):
    response = ollama.chat(
        model="llama3:8b",
        messages=[
            {"role": "system", "content": "You are JARVIS, a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"]
