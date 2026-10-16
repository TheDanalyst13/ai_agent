import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function



def main():
    # API link
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("missing API key")

    # Open library, create client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # setting up input
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # build the message list
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},

    ]
    for _ in range(20):
        # Get response
        response = client.chat.completions.create(
            model="openrouter/free",
            messages = messages,
            tools=available_functions,
            temperature=0,
        )

        # Fail Bailout
        if response.usage is None:
            raise RuntimeError("failed request")

        # Checking for verbose option 
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                if not result_message.get('content'):
                    result_message['content'] = "function completed but no output produced"
                if args.verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
        else:
            print(message.content)
            break
    else:
        print("max iterations reached without a final response")
        raise SystemExit(1)
        


if __name__ == "__main__":
    main()
