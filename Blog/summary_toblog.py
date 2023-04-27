import openai
import os
from time import time,sleep
import textwrap
import re

openai.api_key = "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"

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def gpt3_completion(prompt, engine='text-davinci-002', temp=0.6, top_p=1.0, tokens=2000, freq_pen=0.25, pres_pen=0.0, stop=['<<END>>']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            text = re.sub('\s+', ' ', text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)

if __name__ == '__main__':
    summary = open_file('summary.txt')
    chunks = textwrap.wrap(summary, 2000)
    result = list()
    count = 0
    for chunk in chunks:
        count = count + 1
        prompt = open_file('prompt.txt').replace('<<BLOG>>', chunk)
        prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
        blog = gpt3_completion(prompt)
        print('\n\n\n', count, 'of', len(chunks), ' - ', blog)
        result.append(blog)
    save_file('\n\n'.join(result), 'output_%s.txt' % time())