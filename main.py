from openai import OpenAI
import os, sys

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Set Model/Parameters
model = 'gpt-4o-mini'
temperature = 0.7
max_tokens = 250 # unused by default
messages = []


def chat_with_gpt(prompt):
    # Generate and store response
    messages.append({"role":"user","content":prompt})
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            # max_tokens=max_tokens,  # uncomment for token limit
            temperature=temperature
        )
        msg = response.choices[0].message
        messages.append({"role":msg.role, "content":msg.content})
        return msg.content
    except e as Exception:
        print(e)

if __name__ == "__main__":

    if len(sys.argv) > 1:
        prompt = str([arg + ' ' for arg in sys.argv[1:]])
        print('One-shot: \n\n', chat_with_gpt(prompt), '\n\n')
    else:
        print('Entering Chat..\n')
        while True:
            prompt = input('\nMe: ')
            if prompt.lower() in {'q', 'quit'}:
                print("\nGoodbye!\n\n")
                break
            try:
                response = chat_with_gpt(prompt)
                print(f"GPT-4o: {response}")
            except Exception as e:
                print(f"An error occurred: {e}")
