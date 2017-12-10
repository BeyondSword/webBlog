"""Routers and views for blueprint 'auth'
"""
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .forms import LoginForm
from ..alchemy_model import User

@auth.route("/login/", methods=['GET', 'POST'])
def login():
    """login"""
    login_form = LoginForm()
    if login_form.validate_on_submit:
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember_me.data)
            #print "session user_id is ", session['user_id']
            #print current_user.is_authenticated, current_user.username
            return redirect(request.args.get('next') or
                            url_for('main.index')
                           )
        flash('Invalid username or password.')
    return render_template('login.html', login_form=login_form
                          )

@auth.route("/logout/")
@login_required
def logout():
    """logout"""
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
