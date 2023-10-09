from flask import Flask, request, render_template
import requests
from cachetools import LRUCache
from utils import read_keywords_from_file, write_keyword_to_file
import os

app = Flask(__name__)

cache = LRUCache(maxsize=100)


@app.route('/search', methods=['POST', 'GET'])
def search():
    """
    Handle search requests for news articles.

    Supports both GET and POST methods.
    - GET: Retrieves news articles based on a 'keyword' query parameter.
    - POST: Saves the 'keyword' from the form to a file and retrieves news articles based on the keyword.

    Caches search results to improve performance.

    Returns:
    - If search results are found, renders 'search_result.html' template with the articles.
    - If no results are found, renders 'search_result.html' with an empty list.

    """
    if request.method == 'GET':
        keyword= request.args.get('keyword')

    if request.method == 'POST':
        keyword = request.form.get('keyword')
        write_keyword_to_file(keyword)
    
    cached_data = cache.get(keyword)
    if cached_data:
        data = cached_data
    else:
        NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
        url = f'https://newsapi.org/v2/everything?q={keyword}&apiKey={NEWS_API_KEY}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            cache[keyword] = data
    data = sorted(data.get('articles'), key=lambda x: x["publishedAt"], reverse=True)
    return render_template('search_result.html', search_results=data)
   
    

@app.route('/search-history', methods=['GET'])
def get_search_history():
    """
    Retrieve and display search history.

    Handles GET requests to retrieve a list of previously searched keywords from a file.
    Renders 'search_history.html' template to display the search history.

    Returns:
    - Renders 'search_history.html' with the 'search_history' variable containing the list of keywords.
    """
    return render_template('search_history.html', search_history = read_keywords_from_file())


@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
