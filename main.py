import requests
import smtplib
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

app = Flask(__name__)

posts_list = requests.get('https://api.npoint.io/c790b4d5cab58020d391').json()
my_email = os.getenv("my_email")
password = os.getenv("password")
hotmail_email = os.getenv("hotmail_email")

@app.route('/')
def home():
    return render_template('index.html', posts=posts_list)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        messageEmail = f"name: {name}\nemail: {email} \nphone: {phone}\nmessage: {message}"

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=email,
                to_addrs=hotmail_email,
                msg=f"Subject: Blog message \n\n{messageEmail}"
            )

        return render_template('contact.html', message="Successfully sent your message")
    else:
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
