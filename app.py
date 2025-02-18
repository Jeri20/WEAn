from flask import Flask, render_template, request, jsonify
import sys
import os
import threading
import asyncio  # Import asyncio here
from crawlers.playwright_crawler import crawl_website
from analysis.analyzer import analyze_content

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Render HTML page with form for input

@app.route('/crawl', methods=['POST'])
def crawl():
    url = request.form.get('url')
    # Run the crawl asynchronously in a separate thread
    threading.Thread(target=run_crawl, args=(url,)).start()
    return jsonify({"message": "Crawl started successfully!"})

@app.route('/analyze', methods=['POST'])
def analyze():
    # Run the analysis asynchronously in a separate thread
    threading.Thread(target=run_analysis).start()
    return jsonify({"message": "Analysis completed successfully!"})

# Function to run crawl asynchronously in a separate thread
def run_crawl(url): 
    asyncio.run(crawl_website(url))

# Function to run analysis asynchronously in a separate thread
def run_analysis(): 
    asyncio.run(analyze_content())

if __name__ == '__main__':
    app.run(debug=True)
