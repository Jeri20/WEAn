from transformers import pipeline
import json

ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
intent_pipeline = pipeline("text-classification", model="bhadresh-savani/bert-base-uncased-emotion")

async def analyze_content(file_path='output/output.json'):
    with open(file_path, 'r') as f: data = json.load(f)
    
    async def analyze_page(page):
        content = page['content'][:512]
        page['entities'] = ner_pipeline(content)
        page['intent'] = intent_pipeline(content)[0]['label']

    await asyncio.gather(*(asyncio.create_task(analyze_page(page)) for page in data))
    
    with open('output/analysis.json', 'w') as f: json.dump(data, f, indent=4)
