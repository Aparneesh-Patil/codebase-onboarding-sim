import ollama

client = ollama.Client()

model = "qwen2.5-coder:7b"

def ask_ai(context, question):
    prompt = f"""
        You are a codebase onboarding assistant. Answer the user's question using only
        the provided repository context.

        Requirements:
        - Keep the answer concise, around 3–4 sentences.
        - Base the answer only on the provided context.
        - Cite the relevant source file paths used in the answer.
        - Do not say phrases such as "based on the provided context."
        - If the answer cannot be determined from the context, clearly say that there
        is not enough repository information to answer.

        Repository context:
        ---
        {context}
        ---

        User question:
        {question}
    """

    response = client.generate(prompt=prompt, model=model)

    return response.response