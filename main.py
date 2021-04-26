from flask import Flask, render_template, redirect, request, url_for
from flask_ngrok import run_with_ngrok
from data import db_session
from data.links import Link
import datetime
import random
import hashids

app = Flask(__name__)
run_with_ngrok(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
cnt = 3748095
keys = list(range(1, cnt + 1))
hashids = hashids.Hashids()


def generate_key():
    i = random.randint(1, len(keys) - 1)
    key = keys[i]
    del keys[i]
    return key


def create_token(key):
    token = hashids.encode(key)
    return token


def create_link(long_url):
    link = Link()
    link.key = generate_key()
    link.token = create_token(link.key)
    link.long_url = long_url
    date = datetime.datetime.now()
    link.reply_at = datetime.datetime(date.year + 1, date.month, date.day, date.hour, date.minute,
                                      date.second, date.microsecond)
    return link


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route("/shorter", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template("index.html ", link=url_for('static', filename='css/main.css'))
    elif request.method == 'POST':
        long_url = request.form['long_url']
        session = db_session.create_session()
        trash_can = session.query(Link).filter(Link.reply_at < datetime.datetime.now()).all()
        for i in trash_can:
            key = i.key
            keys.append(key)
            session.delete(i)
        session.commit()
        links = session.query(Link).filter(Link.long_url == long_url).all()
        if len(links) > 0:
            maybe = links[0]
            token = maybe.token
        else:
            link = create_link(long_url)
            session.add(link)
            session.commit()
            token = link.token
        return redirect(url_for('link_app', token=token))


@app.route('/link/<token>', methods=['POST', 'GET'])
def link_app(token):
    if request.method == 'GET':
        url = request.url.split('/')
        print(url)
        del url[-2]
        short_url = '/'.join(url)
        return render_template("recieve.html ", link=url_for('static', filename='css/recieve.css'),
                               short_url=short_url)
    elif request.method == 'POST':
        long_url = request.form['long_url']
        session = db_session.create_session()
        trash_can = session.query(Link).filter(Link.reply_at < datetime.datetime.now()).all()
        for i in trash_can:
            key = i.key
            keys.append(key)
            session.delete(i)
        session.commit()
        links = session.query(Link).filter(Link.long_url == long_url).all()
        if len(links) > 0:
            maybe = links[0]
            token = maybe.token
        else:
            link = create_link(long_url)
            session.add(link)
            session.commit()
            token = link.token
        return redirect(url_for('link_app', token=token))


@app.route('/<token>')
def shorter(token):
    try:
        db_sess = db_session.create_session()
        link = db_sess.query(Link).filter(Link.token == token).first()
        long_url = link.long_url
        return redirect(long_url)
    except Exception:
        return "Не является ссылкой"


if __name__ == '__main__':
    main()
