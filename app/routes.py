
from app import app
import asyncio
from aiohttp import web
from flask import render_template, url_for, flash, redirect,  session, request
from app.forms import LoginForm
from app.utils import get_user_info,   process_async, login_required
from flask_wtf.csrf import CSRFProtect


               
        
# @app.errorhandler(CSRFError)
# def handle_csrf_error(e):
#     app.logger.info(e.description)
#     pass
    
    
    

        


@app.route("/", methods=['GET', 'POST'])

def login():
    form = LoginForm()
    token = form.token.data
    app.logger.info("form token :" + str(token))      
    app.logger.info("form token :" + str(form.csrf_token.data ))    
    app.logger.info("server token : "+ session.get('csrf_token'))
    if session.get('token'):
        app.logger.info("Secret key: "+  app.config['SECRET_KEY'])        
        return redirect(url_for('home', state='active'))    
    if request.method == 'POST' and form.validate_on_submit():
    # if request.method == 'POST':
        token = form.token.data       
        app.logger.info(token) 
        response = get_user_info(token)
        app.logger.info(response)
        if response.status_code == 200:
            session['token'] = form.token.data                           
            return redirect(url_for('home', state='active'))            
        else:
            flash('Não foi possível acessar o sistema. Verifique seu token de acesso e tente novamente', 'danger')
            return render_template('login.html' , form=form)
    app.logger.info('nao validou')
    return render_template('login.html', form=form)



@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))







@app.route('/home/<state>')
@login_required
def home(state):    
    if state == 'active' or state == 'completed':        
        token = session.get('token')
        user = get_user_info(token)
        user = user.json()       
        return render_template('notas.html', user=user, state=state)
    else: 
        session.clear()
        flash('Essa página não foi encontrada. Verifique as informações e tente novamente', 'danger')
        return redirect(url_for('login'))



@app.route('/api/<state>')
@login_required
def api(state):
    token = session.get('token')
    courses = asyncio.run(process_async(token, state))   
    return courses



@app.errorhandler(401)
def error_401(error):
    session.clear()
    flash('Você não possui autorização para acessar esse recurso ou o seu token expirou', 'danger')
    return redirect(url_for('login'))



@app.errorhandler(403)
def error_403(error):
    session.clear()
    flash('Você não possui autorização para acessar esse recurso', 'danger')
    return redirect(url_for('login'))



@app.errorhandler(404)
def error_404(error):
    session.clear()
    flash('Essa página não foi encontrada. Verifique as informações e tente novamente', 'danger')
    return redirect(url_for('login'))



@app.errorhandler(500)
def error_500(error):
    session.clear()
    flash('O Servidor não conseguir responder a essa solicitação. Aguarde alguns minutos e tente novamente', 'danger')
    return redirect(url_for('login'))














