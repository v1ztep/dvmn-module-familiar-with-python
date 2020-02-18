from flask import Flask


def bars_around_user():
    with open('index.html') as file:
      return file.read()

app = Flask(__name__)
app.add_url_rule('/', 'bars around', bars_around_user)
app.run('127.0.0.1')