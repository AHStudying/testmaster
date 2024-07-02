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
    for word in words:
        pronounce_word(word)
        pronounce_definitions(word)
        pronounce_word(word)
        time.sleep(3)  # Wait for 3 seconds between each word

    return redirect(url_for('index'))

def pronounce_word(word):
    tts = gTTS(text=word, lang='en')
    audio_path = f'static/audio/{word}.mp3'
    tts.save(audio_path)
    play_audio(audio_path)

def pronounce_definitions(word):
    url = f'https://www.ahdictionary.com/word/search.html?q={word}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    definitions = []
    for item in soup.find_all('div', class_='ds-list'):
        definitions.append(item.text.strip())
    
    for definition in definitions:
        tts = gTTS(text=definition, lang='en')
        audio_path = f'static/audio/{word}_definition.mp3'
        tts.save(audio_path)
        play_audio(audio_path)

def play_audio(audio_path):
    os.system(f'afplay {audio_path}')  # Mac OS specific, replace with appropriate command for your OS

if __name__ == '__main__':
    app.run(debug=True)
