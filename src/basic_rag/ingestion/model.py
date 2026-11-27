import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

_client = None

def get_client() -> Groq | None:
    global _client
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    if _client is None:
        _client = Groq(api_key=api_key)
    return _client


DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
FALLBACK_MODELS = ["llama-3.1-8b-instant", "qwen/qwen3.8-27b"]


def generate_answer(
    question: str,
    context: str,
    model: str | None = None,
    stream: bool = True
) -> str | None:
    client = get_client()
    if not client:
        print("\n[Notice] GROQ_API_KEY is not set in .env. Skipping LLM generation.")
        return None

    target_model = model or DEFAULT_MODEL

    prompt = f"""Use the following retrieved context to answer the user's question. If the context does not contain enough information to answer, state clearly that the answer cannot be determined from the provided context.

Context:
{context}

Question:
{question}
"""

    models_to_try = [target_model] + [m for m in FALLBACK_MODELS if m != target_model]

    for current_model in models_to_try:
        try:
            response = client.chat.completions.create(
                model=current_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that answers questions accurately based on the provided context."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                stream=stream,
                max_completion_tokens=500
            )

            if stream:
                full_text = []
                for chunk in response:
                    content = chunk.choices[0].delta.content or ""
                    print(content, end="", flush=True)
                    full_text.append(content)
                print()
                return "".join(full_text)
            else:
                answer = response.choices[0].message.content or ""
                print(answer)
                return answer

        except Exception as e:
            if "model_not_found" in str(e) or "404" in str(e):
                continue
            print(f"\n[Notice] Could not complete LLM generation: {e}")
            return None

    print(f"\n[Notice] None of the tried models ({models_to_try}) were available on your Groq account.")
    return None


def model_call():
    client = get_client()
    if not client:
        print("[Notice] GROQ_API_KEY is not set in .env.")
        return

    result = client.chat.completions.create(
        model=DEFAULT_MODEL, 
        messages=[
            {
                "role" : "system", 
                "content" : "Act as Senior Ai engineer"
            }, 
            {
                "role" : "user", 
                "content": "Explain about RAG pipeline basics?"
            }
        ],
        stream=True, 
        max_completion_tokens=500
    )

    for chunk in result:
        content = chunk.choices[0].delta.content or ""
        print(content, end="", flush=True)
    print()
