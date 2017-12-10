"""Routers and views for blueprint 'main'
"""
from tests.log import logger, set_log
from flask_login import login_required
from app.alchemy_model import Post
from app.form import PostForm
from flask import (request, render_template, session, url_for, redirect, flash)
from .import main

@main.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    """depends on method
    GET  direct to where writing new post
    POST process new post submit
    """
    post_form = PostForm()
    if post_form.validate_on_submit():
        post = Post.insert(title=post_form.title.data,
                           content=post_form.content.data,
                           published=post_form.published.data
                          )
        flash('Post created successfully.', 'success')
        if post.published:
            return redirect(url_for('main.detail', slug=post.slug))
        else:
            return redirect(url_for('main.edit', slug=post.slug))
    return render_template('create.html', post_form=PostForm())

@main.route('/<slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    post_form = PostForm()
    #check if method is 'POST' & data is validate
    if post_form.validate_on_submit():
        post.modify(post_form.title.data,
                    post_form.content.data,
                    post_form.published.data
                   )
        flash('Post saved successfully.', 'success')
        if post.published:
            return redirect(url_for('.detail', slug=post.slug))
        else:
            return redirect(url_for('.edit', post=post))
    #flash('Title and Content are required.', 'danger')

    #get data from DB to form
    post_form.title.data = post.title
    post_form.content.data = post.content
    post_form.published.data = post.published
    return render_template('edit.html', post_form=post_form)



@main.route("/<slug>/")
def detail(slug):
    if session.get('logged_in'):
        post = Post.query.filter_by(slug=slug).first_or_404()
    else:
        post = Post.query.filter_by(slug=slug, published=True).first_or_404()
    return render_template('detail.html', post=post)



@main.route('/')
def index():
    """Direct to homepage.
    check whether the browser has logged in
    If loggin in: editing posts is allowed
    If not: it can only read posts

    Support search in future
    """
    #print "session user_id is ", session['user_id']
    #print current_user.is_authenticated, current_user.username

    posts = Post.query_posts()
    return render_template("index.html",
                           posts=posts
                          )
