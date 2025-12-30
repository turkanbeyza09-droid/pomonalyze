# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, session
from app import app 
from analyzer.pomodoro_analyzer import PomodoroAnalyzer 
import os

pomodoro_analyst = PomodoroAnalyzer(default_work_time=25)

@app.route('/')
def index():
    if 'current_target_time' not in session:
        session['current_target_time'] = pomodoro_analyst.default_work_time

    return render_template(
        'index.html', 
        current_target_time=session['current_target_time'],
        history=pomodoro_analyst.history
    )

@app.route('/complete', methods=['POST'])
def complete():
    try:
        actual_time = float(request.form.get('actual_duration'))
    except:
        actual_time = session['current_target_time']
    
    pomodoro_analyst.start_work_session(session['current_target_time'], actual_time)

    new_suggestion = pomodoro_analyst.analyze_and_suggest_time()

    session['current_target_time'] = new_suggestion

    return redirect(url_for('index'))