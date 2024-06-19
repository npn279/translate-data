import json
from time import sleep
import logging

from datasets import load_dataset
from googletrans import Translator

logging.basicConfig(level=logging.INFO, filename='translate.log', filemode='a')

translator = Translator()
dataset = load_dataset('iamnguyen/ultrachat-200k', split='train_sft')

for i in range(0, 100000):
    try:
        conversations = dataset[i]['messages']

        translated_conversations = []
        for message in conversations:
            translated_conversations.append({
                "role": message['role'],
                "content": translator.translate(message['content'], dest='vi').text
            })
            sleep(0.1)
        
        with open(f"data/ultrachat-0_100k.jsonl", 'a', encoding='utf8') as f:
            f.write(json.dumps({
                "idx": i,
                "messages": translated_conversations
            }, ensure_ascii=False) + '\n')
        
        logging.info(f"Translated {i}")
    except Exception as e:
        logging.error(f"Error translating {i}: {e}")
        continue
