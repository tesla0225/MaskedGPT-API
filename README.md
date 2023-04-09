# MaskedGPT-API
When using APIs such as GPT-4, a Wrapper API is used to conceal confidential information.

Edit an .env file in the root directory:
```.env:.env
OPENAI_API_KEY=
LANGUAGE_CODE=ja
MODEL_NAME=gpt-3.5-turbo
```

Build the container:
```code:terminal
docker build -t maskedgpt . 
```

Run:
```code:terminal
docker run -p 8000:8000 maskedgpt 
```

Post in the following format:
```code:terminal
curl -X POST "http://localhost:8000/process_message" -H "Content-Type: application/json" -d '{"message": "文章が入ります"}'
```