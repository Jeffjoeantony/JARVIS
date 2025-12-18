import ollama

def ask_llm(prompt, mode="normal"):
    if mode == "brief":
        system_prompt = (
            "You are JARVIS, a professional AI voice assistant. "
            "Answer briefly in 3 to 4 sentences. "
            "Do NOT roleplay or use fictional references."
        )
    else:
        system_prompt = (
            "You are JARVIS, a professional AI voice assistant. "
            "You are NOT a fictional character. "
            "Do NOT mention Tony Stark, Avengers, or any fictional universe. "
            "If real-world data is missing, say you do not have access."
        )

    response = ollama.chat(
        model="llama3:8b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]
