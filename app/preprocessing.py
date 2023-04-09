from .database import session
from .models import Word


async def request_preprocessing(message: str):
    additional_system_message = "IMPORTANT: include a word and its description as (word): (description). Do NOT use (description) in the output.  "
    words = session.query(Word).all()
    for word in words:
        if word.word in message:
            message = message.replace(word.word, word.cryptoword)
            additional_system_message += f" {word.cryptoword}: {word.description}"
    print("message:", message)
    print("additional_system_message:", additional_system_message)
    return message, additional_system_message
