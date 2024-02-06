# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Привіт, світ! Це бекенд на Python і він працює!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
