
from app import app
import json
import requests
import aiohttp
from aiohttp import web
import asyncio
from flask import render_template, url_for, flash, redirect, request, session
from datetime import datetime
from functools import wraps
from app.forms import LoginForm
# from app.models import User






async def fetch(session, url, token):
    async with session.get(url, headers={'Accept': 'application/json', 'Authorization': 'Bearer ' + token}) as response:
        response = await response.json()        
        return response
    
    
    
    
    

async def get_course_data(session, course, token):
    
    course_id = course['id']
    course_name = course['name']
    url = f'https://pucminas.instructure.com/api/v1/courses/{course_id}/students/submissions?include[]=rubric_assessment&include[]=assignment&per_page=5000'
    response = await fetch(session, url, token)
    data = {
        'course_name': course_name,
        'course_id': course_id
    }
    try:
        courses_formated, is_project = format_courses(response)
        data['is_project'] = is_project        
        data['assignments'] = courses_formated   
        
    except Exception as e:        
        app.logger.error(f"Erro ao processar dados: {e}")
    

    return data




def format_courses(response):
    data = []
    is_project = False
    for res in response:
            due_data = ''        
            if 'due_at' in res['assignment'] and res['assignment']['due_at'] :
                due_date = res['assignment']['due_at']
            else:
                data_temp =  datetime.now()
                due_date = data_temp.strftime("%Y-%m-%dT%H:%M:%SZ")
            
            
            assignment_data = {
                'assignment_id': res['assignment']['id'] if 'assignment' in res and 'id' in res['assignment'] else None,
                'assignment_name': res['assignment']['name'] if 'assignment' in res and 'name' in res['assignment'] else None,
                'points_possible': res['assignment']['points_possible'] if 'assignment' in res and 'points_possible' in res['assignment'] else None,
                'entered_score': res['entered_score'] if 'entered_score' in res else None,                
                'html_url': res['assignment']['html_url'] if 'assignment' in res and 'html_url' in res['assignment'] else None,
                'rubrics': [],
                'due_date': due_date
            }
            
            rubric_assessment_data = []
            if isinstance(res.get('rubric_assessment'), dict):                
                dict_rubric = res.get('rubric_assessment')
                for key, values in dict_rubric.items():
                    rubric_points = {                        
                    'rubric_id': key,
                    "points":  values.get('points')
                    }                            
                    rubric_assessment_data.append(rubric_points)  
                
            # Verifica se 'assignment' existe em 'res' e se 'rubric' é uma lista não vazia
            if 'assignment' in res and 'rubric' in res['assignment'] and isinstance(res['assignment']['rubric'], list):
                for r in res['assignment']['rubric']:
                    rubrics_data = {
                        'id': r.get('id', None),
                        'description': r.get('description', None),
                        'long_description': r.get('long_description', None),
                        'point': rubric_point(rubric_assessment_data, r.get('id', None))
                        # Se você tem duas vezes 'long_description', talvez tenha sido um engano, ajuste conforme necessário
                    }
                    assignment_data['rubrics'].append(rubrics_data)
                    is_project = True
            data.append(assignment_data)
    
    sorted_assignments = sorted(data, key=lambda x: x['due_date'], reverse=False)
    return sorted_assignments, is_project



def grade_courses(token, courses):
    all_grade = []
    for course in courses:
        c = {}
        grades = courses_assignments(token, str(course['id']))
        c['name'] = course['name']
        c['grade'] = []
        for grade in grades:
            grade_dict = {}
            grade_dict ['id'] = grade['id']           
            grade_dict ['score'] = grade['score']
            grade_dict ['entered_score'] = grade['entered_score']
            grade_dict ['approved'] = 'true' if grade['score']== grade['entered_score'] else grade_dict ['approved'] == 'false'
            c['grade'].append(grade_dict)
        all_grade.append(c)
    return all_grade  



def rubric_point(rubric_data, rubric_id):
    points_ = None   
    for item in rubric_data:
        if item.get('rubric_id') == rubric_id:
            points_ = item.get('points')
    return points_



def courses_assignments(token, course_id):
    url = 'https://pucminas.instructure.com/api/v1/courses/'+ course_id + '/students/submissions'
    response = requests.get(
        url,
        headers={
        'Accept': 'application/json',
        'Authorization': 'Bearer '+ token
    }
    )      
    return response.json()



def courses_rubrics(course_id, assignments_id):
    url = 'https://pucminas.instructure.com/api/v1/courses/' + course_id + '/assignments/'+ assignments_id + '/submissions/self?include[]=full_rubric_assessment&per_page=1000'   
    response = requests.get(
        url,
        headers={
        'Accept': 'application/json',
        'Authorization': 'Bearer '+ TOKEN
    }
    )      
    return response.json()




        








async def get_courses_info(token, state):
    url = 'https://pucminas.instructure.com/api/v1/users/self/courses?enrollment_state=' + state + '&per_page=5000'
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, url, token)
        tasks = [get_course_data(session, course, token) for course in response]
        return await asyncio.gather(*tasks)
    
    
        

def get_completed_courses_info(token):
    url = 'https://pucminas.instructure.com/api/v1/users/189649/courses?per_page=5000&enrollment_state=completed'  
    response = requests.get(
        url,
        headers={
        'Accept': 'application/json',
        'Authorization': 'Bearer '+ token
    }
    )      
    return response.json()




def get_user_info(token):
    try:
        url = 'https://pucminas.instructure.com/api/v1/users/self'  
        response = requests.get(
            url,
            headers={
            'Accept': 'application/json',
            'Authorization': 'Bearer '+ token
        }
        )
    except:
        return redirect(url_for('logout'))
    return response



async def process_async(token, state):
    async with aiohttp.ClientSession() as session:
        courses = await get_courses_info(token, state)
        return courses
    
    

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = get_user_info(session.get("token")) 
        if session.get("token") == None or response.status_code != 200:
            # app.logger.info("test" + session.get("token"))
            session.clear()
            flash('Não foi possível acessar o sistema. Verifique seu token de acesso e tente novamente', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
    









 
    