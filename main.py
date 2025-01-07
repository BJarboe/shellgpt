from openai import OpenAI
import os, sys

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Set Model/Parameters
model = 'gpt-4o-mini'
temperature = 0.7
messages = []

def sys_context() -> None:
    prompt_path = '/home/delloid/projects/python/chatgpt/.prompt'
    with open(prompt_path, 'r') as file:
        prompt = file.read()
    chat_with_gpt(prompt, role='system')

def chat_with_gpt(prompt: str, role='user') -> None:
    # Generate and store response
    messages.append({'role':role,'content':prompt})
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        msg = response.choices[0].message
        messages.append({'role':msg.role, 'content':msg.content})
        return msg.content
    except Exception as e:
        return e


if __name__ == '__main__':
    sys_context()
    if len(sys.argv) > 1:
        prompt = ''.join([arg + ' ' for arg in sys.argv[1:]])
        print('One-shot: \n\n', chat_with_gpt(prompt), '\n\n')
    else:
        print('Entering Chat..')
        while True:
            prompt = input('\nMe: ')
            if prompt.lower() in {'q', 'quit'}:
                print('Goodbye!\n')
                break
            try:
                response = chat_with_gpt(prompt)
                print(f'GPT-4o: {response}')
            except Exception as e:
                print(f'An error occurred: {e}')