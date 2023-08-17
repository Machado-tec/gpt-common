#!/usr/bin/env python3

import argparse
import openai
from openai import ChatCompletion  # Importação já está correta
from env import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def call_openai(prompt, filenames, max_tokens):
    messages = [{"role": "system", "content": "Input files: " + ', '.join(filenames)}]
    messages.extend(prompt)

    response = ChatCompletion.create(
        model="gpt-4",  # Atualize para um modelo GPT-4 disponível
        messages=messages,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )

    if response['choices']:
        answer = response['choices'][0]['message']['content'].strip()
        return answer
    else:
        return "Erro: não foram encontradas escolhas na resposta do ChatGPT."

# Restante do código permanece inalterado


def read_files(filepaths):
    prompts = []
    for filepath in filepaths:
        with open(filepath, "r") as f:
            prompts.append({"role": "user", "content": f"File: {filepath}\n{f.read().strip()}"})
    return prompts

def save_messages_to_file(answer, output_file):
    with open(output_file, "w") as f:
        f.write(answer)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script para chamar a API da OpenAI.")
    parser.add_argument("-t", "--type", type=str, choices=["s", "m", "l"], default="s", help="Tipo de resposta (s: curta, m: média, l: longa)")
    parser.add_argument("-m", "--message", type=str, help="Mensagem a ser enviada para o ChatGPT.")
    parser.add_argument("-f", "--files", type=str, nargs='*', default=[], help="Caminho para os arquivos com os prompts.")
    parser.add_argument("-o", "--output", type=str, help="Arquivo de saída para salvar a resposta do ChatGPT.")

    args = parser.parse_args()

    if args.message:
        prompts = [{"role": "user", "content": args.message}]
    else:
        prompts = []

    prompts.extend(read_files(args.files))

    if args.type == "s":
        max_tokens = 50
    elif args.type == "m":
        max_tokens = 1024
    else:  # args.type == "l"
        max_tokens = 2048

    answer = call_openai(prompts, args.files, max_tokens)
    

    if args.output:
        save_messages_to_file(answer, args.output)
    else:
        print(answer)
