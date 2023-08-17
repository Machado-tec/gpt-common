#!/usr/bin/env python3

import argparse
import openai
from openai import ChatCompletion  
from env import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

import time


def call_openai(prompt, max_tokens=2048, translate=False, compare=False):
    for _ in range(5):  # tente novamente até 5 vezes
        try:
            if translate:
                system_message = f"You are a helpful assistant. Translate the following text to Portuguese:\n{prompt}"
                user_message = "Please translate."
            else:
                if not compare:
                    system_message = f"You are a helpful assistant. Summarize the following student inputs:\n{prompt}"
                    user_message = "Please summarize."
                else: 
                    system_message = f"You are a great teacher's assistant.Compare the class summary with the summary made by this student. Evaluate the student's adherence based on their summary compared to the class syllabus. Class Summary:{prompt[0]} Student: {prompt[1]}"
                    user_message = "Dear Artificial Intelligence, could you please provide compliments to the student to boost their self-esteem and point out some areas where they need improvement? We aim to build a conducive learning and growth environment for students, so it is important to balance positive feedback with some points they need to work on. Thank you."
                    print("compare=True")
                    print("="*60)
                    print("<>"*60)
                    print("Resumo com o prompt do aluno")
                    print("prompt[0]",prompt[0])
                    print("="*60)
                    print("="*60)
                    print("prompt[1]",prompt[1])
                    print("="*60)
                    print("()"*60)

            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": system_message
                    },
                    {
                        "role": "user",
                        "content": user_message
                    },
                ],
                max_tokens=max_tokens,
            )

            if response['choices']:
                answer = response['choices'][0]['message']['content'].strip()
                return answer
            else:
                return "Erro: não foram encontradas escolhas na resposta do ChatGPT."
        except openai.error.RateLimitError:
            print("Excedido o limite de solicitações para a API OpenAI. Aguardando antes de tentar novamente...")
            time.sleep(60)  # espere 60 segundos antes de tentar novamente



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
# Genie, transforme este codigo em um codigo que eu possa tornar publico e que seja generico para o uso do chatgpt. 
# Preserve os parametros, mas elimine o que é particular do uso atual. 
# Ao final, o codigo deve ser compilado para que ele possa ser usado em qualquer lugar.