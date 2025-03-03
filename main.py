import requests
from flask import Flask, render_template

app = Flask(__name__)

posts_list = requests.get('https://api.npoint.io/c790b4d5cab58020d391').json()

@app.route('/')
def home():
    return render_template('index.html', posts=posts_list)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/post/<number>')
def post(number):
    selected_post = None
    for i in posts_list:
        if i['id'] == int(number):
            selected_post = {
                'id': i['id'],
                'title': i['title'],
                'subtitle': i['subtitle'],
                'body': i['body']
            }
    return render_template('post.html', post=selected_post)
if __name__ == '__main__':
    app.run(debug=True)
