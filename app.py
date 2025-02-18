import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from flask import Flask, render_template, request, jsonify
from crawlers.playwright_crawler import crawl_website
from analysis.analyzer import analyze_content
import asyncio

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crawl', methods=['POST'])
async def crawl():
    url = request.form['url']
    await crawl_website(url)
    return jsonify({"message": "Crawl completed!"})

@app.route('/analyze', methods=['POST'])
async def analyze():
    await analyze_content()
    return jsonify({"message": "Analysis completed!"})

if __name__ == "__main__":
    app.run(debug=True)
