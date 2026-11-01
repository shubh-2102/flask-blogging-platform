from flask import render_template, redirect, url_for, flash
from app.blueprints.auth import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Will be fully wired with Flask-WTF forms and Flask-Login in Week 2
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Will be fully wired with Flask-WTF forms and Flask-Login in Week 2
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
