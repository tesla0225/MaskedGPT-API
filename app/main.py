import os
import openai
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from .database import session
from .preprocessing import request_preprocessing
from .postprocessing import response_postprocessing

load_dotenv()

language_code = os.environ.get("LANGUAGE_CODE", "ja")
model_name = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")
openai_api_key = os.environ.get("OPENAI_API_KEY", "")
openai.api_key = openai_api_key

language_type = {
    "ja": "Japanese",
    "en": "English",
}

system_message_sent = False

app = FastAPI()


@app.post("/process_message")
async def process_message(request: Request):
    global system_message_sent

    data = await request.json()
    message = data["message"]

    # 前処理
    processed_message, additional_system_message = await request_preprocessing(message)

    messages = [{"role": "user", "content": processed_message}]

    if not system_message_sent:
        messages.insert(
            0, {"role": "system", "content": f"ChatGPT is an OpenAI language model. Follow instructions, use markdown for responses, and Output in {language_type}."})
        system_message_sent = True

    messages.insert(
        0, {"role": "system", "content": additional_system_message})

    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages,
    )

    # 後処理
    final_message = await response_postprocessing(response.choices[0]["message"]["content"])
    response.choices[0]["message"]["content"] = final_message
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
