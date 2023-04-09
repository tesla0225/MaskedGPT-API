import re
from .database import session
from .models import Word


async def response_postprocessing(message: str):
    cryptowords_in_message = set(re.findall(r'#\{\w{8}\}', message))
    for cryptoword in cryptowords_in_message:
        word = session.query(Word).filter(
            Word.cryptoword == cryptoword).first()
        if word:
            message = message.replace(word.cryptoword, word.word)
    return message
