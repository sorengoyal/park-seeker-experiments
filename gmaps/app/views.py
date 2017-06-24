from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

@app.route('/')
def index():
    
    return render_template('index.html', key = app.config['MAPS_API_KEY'] )
