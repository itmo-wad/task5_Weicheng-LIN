from flask import Flask, flash, redirect, render_template, request, session, abort, url_for

from markupsafe import escape

from flask_pymongo import PyMongo

from . forms import LoginForm

from app import app


app.config['MONGO_URI']="mongodb://localhost:27017/stevenDB"

mongo = PyMongo(app)

key = b'\xd4\x87\\\x0eJ\x80\x9em=\r\x91d\x9b\xe3c'

@app.route('/')
def index():
    if session['username']:
        return render_template('index.html')
    else:
        flash('You are not authenticated')
    return redirect(url_for('login'))


@app.route('/cabinet')
def cabinet():
    if session['username']:
        return redirect(url_for('cabinet'))
    else:
        flash('You are not authenticated')
    return redirect(url_for('login'))


@app.route('/images/<path:filename>')
def imgFile(filename):
    if session['username']:
        return send_from_directory('/static/images', filename)
    else:
        flash('You are not authenticated')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if session['username']:
            return  redirect(url_for('index'))
    except Exception:
        pass
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = form.username.data
        login_user = mongo.db.users.find_one({'username':user})
        if login_user is None:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        session['username'] = True
        return redirect(url_for('index'))
    return render_template('login.html', form=form)