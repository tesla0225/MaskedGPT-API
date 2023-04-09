import pandas as pd
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Word, Base


def generate_cryptoword(word: str) -> str:
    return f"#{{{str(uuid.uuid4())[:8]}}}"


csv_path = "./dict.csv"
df = pd.read_csv(csv_path)

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
