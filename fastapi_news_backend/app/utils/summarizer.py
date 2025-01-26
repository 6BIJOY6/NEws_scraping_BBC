import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
# Print the current working directory for debugging
# print(f"Current working directory: {os.getcwd()}")
gro_api_key = os.getenv("GROQ_API_KEY")

print(f"GROQ_API_KEY: {gro_api_key}")
if not gro_api_key:
    raise ValueError("GROQ_API_KEY is not set. Please ensure it's set in the .env file.")

def generate_summary(news_body: str) -> str:
    client = Groq(api_key=gro_api_key)
    chat_completion = client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in news summarization in Bengali languages. Please summarize the following news article in 3-5 bullet points in Bengali."
            },
            {"role": "user", "content": news_body}
        ],
        temperature=0,
        max_tokens=2000,
        top_p=1,
        stream=False,
    )
    return chat_completion.choices[0].message.content
