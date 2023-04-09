import requests
import os
import re
import uuid
import pandas as pd
import openai
from fastapi import FastAPI, Request, Response
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

language_code = os.environ.get("LANGUAGE_CODE", "ja")
model_name = os.environ.get("MODEL_NAME", "gpt-4")
openai_api_key = os.environ.get("OPENAI_API_KEY", "")
openai.api_key = openai_api_key

system_message_sent = False

def generate_cryptoword(word: str) -> str:
    return f"#{{{str(uuid.uuid4())[:8]}}}"

csv_path = "./dict.csv"
df = pd.read_csv(csv_path)
Base = declarative_base()


class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True)
    word = Column(String)
    description = Column(String)
    cryptoword = Column(String)


engine = create_engine("sqlite:///words.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

session = Session()
for index, row in df.iterrows():
    existing_word = session.query(Word).filter(
        Word.word == row["word"]).first()
    if not existing_word:
        cryptoword = generate_cryptoword(row["word"])
        word = Word(
            word=row["word"], description=row["description"], cryptoword=cryptoword)
        session.add(word)
session.commit()

app = FastAPI()


@app.post("/process_message")
async def process_message(request: Request):
    global system_message_sent  # グローバル変数を参照

    data = await request.json()
    message = data["message"]

    # 前処理
    processed_message, additional_system_message = await request_preprocessing(message)

    messages = [{"role": "user", "content": processed_message}]

    # システムメッセージが未送信の場合、メッセージリストに追加し、送信済みに設定
    if not system_message_sent:
        messages.insert(
            0, {"role": "system", "content": "ChatGPT is an OpenAI language model. Follow instructions, use markdown for responses, and Output in Japanese."})
        system_message_sent = True

    messages.insert(
        0, {"role": "system", "content": additional_system_message})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )

    # 後処理
    final_message = await response_postprocessing(response.choices[0]["message"]["content"])
    response.choices[0]["message"]["content"] = final_message
    return response

# 3. 前処理と後処理の実装


async def request_preprocessing(message: str):
    additional_system_message = "include a word and its description as (word): (description) "
    words = session.query(Word).all()
    for word in words:
        if word.word in message:
            message = message.replace(word.word, word.cryptoword)
            additional_system_message += f" {word.cryptoword}: {word.description}"
    print("request_preprocessing:", message)
    print("request_preprocessing_add:", additional_system_message)
    return message, additional_system_message


async def response_postprocessing(message: str):
    cryptowords_in_message = set(re.findall(r'#\{\w{8}\}', message))
    for cryptoword in cryptowords_in_message:
        word = session.query(Word).filter(
            Word.cryptoword == cryptoword).first()
        if word:
            message = message.replace(word.cryptoword, word.word)
    return message

# 4. FastAPIアプリの起動
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
