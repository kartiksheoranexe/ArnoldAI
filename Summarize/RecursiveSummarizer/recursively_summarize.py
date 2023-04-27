import openai
from youtube_transcript_api import YouTubeTranscriptApi
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

def get_transcript(url):
    # Extract the video ID from the URL using a regular expression
    match = re.search(r"v=([A-Za-z0-9_-]{11})", url)
    if match:
        video_id = match.group(1)
    else:
        print("Invalid YouTube video URL.")
        exit()

    # Get the transcript for the video
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    except:
        print("Transcript not available for this video.")
        exit()

    # Convert the transcript list to plain text
    transcript = ""
    for i in transcript_list:
        transcript += i["text"] + " "

    return transcript

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
            filename = '%s_gpt3.txt' % time()
            with open('gpt3_logs/%s' % filename, 'w') as outfile:
                outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=iw97uvIge7c"
    transcript = get_transcript(url)
    chunks = textwrap.wrap(transcript, 2000)
    result = list()
    count = 0
    for chunk in chunks:
        count = count + 1
        prompt = open_file('prompt.txt').replace('<<SUMMARY>>', chunk)
        prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
        summary = gpt3_completion(prompt)
        print('\n\n\n', count, 'of', len(chunks), ' - ', summary)
        result.append(summary)
    save_file('\n\n'.join(result), 'output_%s.txt' % time())