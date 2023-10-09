from flask import Flask, request, jsonify, render_template
import requests
from cachetools import LRUCache

app = Flask(__name__)

cache = LRUCache(maxsize=100)

NEWS_API_KEY = '076f13668fe345808c5cb5facf6e6eed'


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        keyword= request.args.get('keyword')

    if request.method == 'POST':
        keyword = request.form.get('keyword')
        with open('searched_keywords.txt', 'a') as file:
            keywords = read_keywords()
            if keyword not in keywords:
                file.write(keyword + "\n")
    
    cached_data = cache.get(keyword)
    if cached_data:
        data = cached_data
    else:
        url = f'https://newsapi.org/v2/everything?q={keyword}&apiKey={NEWS_API_KEY}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            cache[keyword] = data

    return render_template('search_result.html', search_results=data.get('articles'))
   
    

@app.route('/search-history', methods=['GET'])
def get_search_history():
    return render_template('search_history.html', search_history = read_keywords())
    
def read_keywords():
    with open('searched_keywords.txt', 'r') as file:
        keywords = file.read().splitlines()
    return keywords


@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
