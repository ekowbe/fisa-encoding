"""module to handle front end"""
#!/usr/bin/env python

# -----------------------------------------------------------------------
# reg.py
# Author: Ekow Bentsi-Enchill
# -----------------------------------------------------------------------

from time import strftime
from datetime import datetime
import json
from flask import Flask, request, make_response, render_template

# -----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')

# -----------------------------------------------------------------------

# -----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    """home page"""

    html = render_template('index.html')
    response = make_response(html)
    return response

@app.route('/check_FISA', methods=['GET'])
def check_FISA():
    print(request.view_args)
    # print(request.form.get())
