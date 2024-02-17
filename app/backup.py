
from app import app, db
import json
import aiohttp
import asyncio
import requests
from flask import render_template, url_for, flash, redirect, request, session
from app.forms import LoginForm
from app.utils import process_async, get_user_info
from app.models import User


TOKEN = '11748~boVwPRgngLfb55Ku1kEYTl7c1qEkgD62M62cTO2IwbyPbSXqQJMOUFlGT0hInuqC'

COURSES = []



    

# Rota do Flask
@app.route('/active')
@app.route('/home/<state>')
def home(state):
    # token = session.get('token')
    user = get_user_info(token)   
    return render_template('notas.html', user=user, state=state)



# @app.route('/')
# def index():
#     token = TOKEN
#     user = get_user_info(token) 
#     return render_template('notas.html', user=user)

# @app.route('/test')
# def test():
#     return COURSES


@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html', form=form)




@app.route('/api/<state>')
def api(state):
    token = TOKEN
    courses = asyncio.run(process_async(token, state))
    return courses










# @app.route("/", methods=['GET', 'POST'])
# async def login():
#     form = LoginForm()
#     if session.get('token'):
#         return redirect(url_for('home', state='active'))
#     if form.validate_on_submit():
#         token = form.token.data
#         user_ = get_user_info(token)  # Chama a função para pegar informações do usuário
#         if user_:
#             session['token'] = form.token.data                           
#             return redirect(url_for('home', state='active'))            
#         else:
#             flash('Não foi possível acessar o sistema. Verifique seu token de acesso e tente novamente', 'danger')
#             return render_template('login.html' , form=form)
#     return render_template('login.html', form=form)




# @app.route("/update_courses/", methods=['GET'])
# def update_courses(id):
#     courses = get_activate_courses_info(session['token'])
#     app.logger.info(courses)
#     json_str = json.dumps(courses)
#     user = User.query.filter_by(id_user = id).first()
#     user.courses_activate = json_str
#     db.session.commit()
#     return redirect(url_for('login'))  














