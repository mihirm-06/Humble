# import requirements needed
import os
from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from utils import get_base_url
import aitextgen
from aitextgen import *
import json
import string
from random import randint
import random
#import nltk
#from nltk.tokenize import word_tokenize as tw
#nltk.download('punkt')


# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)

# Loading model
nk_ai = aitextgen(model_folder="model/nk_ai")
gr_ai = aitextgen(model_folder="model/gr_ai")
dt_ai = aitextgen(model_folder="model/dt_ai")
sp_ai = aitextgen(model_folder="model/sp_ai")

# History list
gen_results = []

# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')
app.secret_key = os.urandom(64)

def fix_grammar(input):
    end_punc = '.?!'
    no_first_letter = True
    fixed_grammar = ''
    index = 0
    for index in range(len(input)):
        char = input[index]
        if char not in string.ascii_letters and no_first_letter:
            #if the first character isn't a letter, it ignores it until it finds a letter
            continue
        elif char in string.ascii_letters and no_first_letter:
            #if it finds the first letter, it adds it to the edited version
            no_first_letter = False
            char = char.upper()
            fixed_grammar += (char)
        elif char == ',' and input[index+1] != ' ':
            #if it findas a comma with no space after it, it will add the comma and a space to the edited version
            fixed_grammar += ', '
        elif char == ' ' and input[index+1] == ' ':
            #if it detects a double space it doesnt add the first space, and so on until there's only one space
            continue
        else:
            fixed_grammar += (char)
        if char in end_punc:
            break
    return(fixed_grammar)

# set up the routes and logic for the webserver
@app.route(f'{base_url}')
def home():
    if len(gen_results) > 0:
        output = "<ol style= \"color: white; text-align: center; list-style-position: inside;\">"
        for sent in gen_results:
            new_sent = "<li>" + sent + "\n"
            output += new_sent
        output += "</ol>"
        return render_template('home.html', generated = output)
    else:
        return render_template('home.html', generated = None)


    
# @app.route(f'{base_url}/home')
# def history():
#     return render_template('history.html')

@app.route(f"{base_url}/teams")
def teams():
    return render_template("teams.html")

# define additional routes here
# for example:
@app.route(f'{base_url}', methods=["POST"])
def home_model():
    return redirect(url_for("model"))

@app.route(f'{base_url}', methods=["POST"])
def home_post():
    return redirect(url_for("about"))

### Kennedy starts here
@app.route(f'{base_url}/models/')
def models():
    if 'data' in session:
        data = session['data']
        return render_template('models.html', generated = data)
    else:
        return render_template('models.html', generated = None)

#def get_model():
#    which_model = json.loads(model_to_use)
#    return which_model

@app.route(f'{base_url}/generate_text', methods=["POST"])
def generate_text():
    #if request.method == 'POST':
    #    which_model = request.json['which_model']

    prompt = request.form['prompt']
    which_model = request.form['model']
    model_str = str(which_model)

    if model_str == "🥩":
        model = gr_ai
    elif model_str == "🍊":
        model = dt_ai
    elif model_str == "💅":
        model = nk_ai
    elif model_str == "🎭":
        model = sp_ai
    else:
        num = randint(0, 3)
        if num == 0:
            model = gr_ai
        elif num == 1:
            model = dt_ai
        elif num == 2: 
            model = nk_ai
        else:
            model = sp_ai


    generated = model.generate(n=1,
                              batch_size=5,
                              prompt = str(prompt),
                              min_length=10,
                              max_length=100,
                              temperature=1,
                              top_p=0.9,
                              return_as_list=True)
    # Here
    
    result = fix_grammar(generated[0])
    gen_results.append(result)
    
    with open('history.txt', 'a+') as f:
        f.write(result)
        f.write('\n')
    f.close()
    
    data = {'generated_1s' : result}
    session['data'] = result
    return redirect(url_for('models'))

# ### Kennedy/Jacq starts here
@app.route(f'{base_url}/history/')
def history():
    if len(gen_results) > 0:
        output = "<ol style= \"color: white; text-align: left;\">"
        for sent in gen_results:
            new_sent = "<li>" + sent + "</li>"
            output += new_sent
        output += "</ol>"
    else:
        output = None

    if 'find' in session:
        data = session['find']
        print(data)
        if data != "N/A":
            random.shuffle(data)
            history_data = "<ol style= \"color: white; text-align: left;\">"
            for sent in data:
                new_sent = "<li>" + sent + "\n"
                history_data += new_sent
            history_data += "</ol>"
            return render_template('history.html', generated = history_data, history = output)
        else:
            return render_template('history.html', generated = "<b>I couldn't find what you were looking for, DOOSHBAGGG</b>", history = output)
    else:
        return render_template('history.html', generated = None, history = output)

@app.route(f'{base_url}/search', methods=["POST"])
def search():
    keywords = request.form['prompt']
    history_list = []
    # Read stuff
    with open('history.txt', 'r') as f:
        history_list = f.readlines()
    f.close()
    # Find
    find = False
    history_find = []
    for sent in history_list:
        if str(keywords) in sent:
            history_find.append(sent)
            find = True
    if not find:
        session['find'] = "N/A"
    else:
        session['find'] = history_find
    return redirect(url_for('history'))

if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'cocalcg25.ai-camp.dev'
    
    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host = '0.0.0.0', port=port, debug=True)

