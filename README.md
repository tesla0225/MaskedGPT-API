# MaskedGPT-API
When using APIs such as GPT-4, a Wrapper API is used to conceal confidential information.

## Example
Input:
```terminal:terminal
curl -X POST "http://localhost:8000/process_message" -H "Content-Type: application/json" -d '{"message": "Based on the following passage, please output a job advertisement for OpenAI. ChatGPT is a large language model based on the GPT-3.5 architecture developed by OpenAI. OpenAI is one of the leading companies in the field of artificial intelligence and machine learning. Microsoft utilizes its technology through a partnership with OpenAI. Bing, operated by Microsoft, competes with Google as a search engine."}'
```

After conversion using the Wrapper API (part of what is being sent to the GPT-4 API):
```
Based on the following passage, please output a job advertisement for #{088e71b0}. #{cc93b624} is a large language model based on the GPT-3.5 architecture developed by #{088e71b0}. #{088e71b0} is one of the leading companies in the field of artificial intelligence and machine learning. #{e9449149} utilizes its technology through a partnership with #{088e71b0}. #{856919e5}, operated by #{e9449149}, competes with #{d6b5ce15} as a search engine.
```

Output (response from the GPT-4 API):
```terminal:terminal
{"id":"XXXX","object":"chat.completion","created":YYYYY,"model":"gpt-4-0314","usage":{"prompt_tokens":259,"completion_tokens":434,"total_tokens":693},"choices":[{"message":{"role":"assistant","content":"Job Advertisement: AI Application Developer at OpenAI\n\nAre you passionate about artificial intelligence and machine learning? Join our team at OpenAI and help us revolutionize the field!\n\nAbout Us:\nWe are a leading company in the realm of AI and machine learning, responsible for the development of the groundbreaking ChatGPT. As a large language model based on the GPT-3.5 architecture, our technology powers innovative applications like the chat-driven AI utilized by our partner, Microsoft, who operates the competitive search engine Bing.\n\nYour Role:\nAs an AI Application Developer at OpenAI, you will develop and improve our cutting-edge AI applications. You will work closely with both our in-house team and our partners like Microsoft, enabling us to further our reach within various industries competing with companies like Google.\n\nResponsibilities:\n- Design, develop, and maintain AI applications using our GPT-3.5-based language model, ChatGPT\n- Collaborate with cross-functional teams to integrate AI capabilities in various projects\n- Conduct research to stay up-to-date with the latest advancements in AI and machine learning\n- Contribute innovative ideas to enhance our product offerings and user experiences\n\nRequirements:\n- Bachelor's or Master's degree in Computer Science, Engineering, or a related field\n- Strong knowledge of AI and machine learning, with proficiency in Python or similar languages\n- Familiarity with the GPT-3.5 architecture and natural language processing techniques\n- Excellent problem-solving and communication skills\n\nWhy Join OpenAI?\n- Be a part of a dynamic, innovative team dedicated to revolutionizing the field of AI\n- Work on cutting-edge projects with partners such as Microsoft\n- Competitive salary, benefits, and opportunities for professional growth\n\nDon't miss this opportunity to be a part of a company shaping the future of artificial intelligence! Apply now and contribute to the success of OpenAI and our partnership with Microsoft."},"finish_reason":"stop","index":0}]}
```

## How to use

1. Please edit the dict.csv file and enter the words you want to encrypt.


2. Edit an .env file in the root directory:
```.env:.env
OPENAI_API_KEY=
LANGUAGE_CODE=ja
MODEL_NAME=gpt-3.5-turbo
```

3. Build the container:
```code:terminal
docker build -t maskedgpt . 
```

4. Run:
```code:terminal
docker run -p 8000:8000 maskedgpt 
```

5. Post in the following format:
```code:terminal
curl -X POST "http://localhost:8000/process_message" -H "Content-Type: application/json" -d '{"message": "Input Text"}'
```