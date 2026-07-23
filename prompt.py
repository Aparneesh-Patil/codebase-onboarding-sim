import ollama

client = ollama.Client()

model = "qwen2.5-coder:7b"

def ask_ai(context, question):
    prompt = "Answer the following question: " + question + ". Use the following context and sources and give me a short summary, around 3-4 sentences, and also source your answer, and don't say anything like 'in the context provided'. Here is the context: " + context + "."

    response = client.generate(prompt=prompt, model=model)

    print(response.response)