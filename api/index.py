from flask import Flask, render_template, request, redirect, url_for
from gtts import gTTS
from bs4 import BeautifulSoup
import os
import requests
import random
import time

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        words = request.form['words'].strip().split('\n')
        random.shuffle(words)
        return render_template('contest.html', words=words)
    return render_template('index.html')

@app.route('/contest', methods=['POST'])
def contest():
    words = request.form.getlist('words[]')
    return render_template('contest.html', words=words)

@app.route('/pronounce', methods=['GET'])
def pronounce():
    word = request.args.get('word')
    tts = gTTS(text=word, lang='en')
    audio_data = tts.get_audio_data()
    return audio_data, 200, {'Content-Type': 'audio/mpeg'}

@app.route('/definition', methods=['GET'])
def definition():
    word = request.args.get('word')
    url = f'https://www.ahdictionary.com/word/search.html?q={word}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    definitions = []
    for item in soup.find_all('div', class_='ds-list'):
        definitions.append(item.text.strip())
    
    combined_definition = '\n'.join(definitions)
    tts = gTTS(text=combined_definition, lang='en')
    audio_data = tts.get_audio_data()
    return audio_data, 200, {'Content-Type': 'audio/mpeg'}

if __name__ == '__main__':
    app.run(debug=True)
