# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Привіт, світ! Це мій перший бекенд на Python з Flask і він працює!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
