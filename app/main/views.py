from .import main
from flask import (request, render_template, session, url_for, redirect, flash)
import functools
from test.log import logger, set_log
from app.model import Entry, FTSEntry
from playhouse.flask_utils import object_list

from manage import app

#define decorator   check if user has logged in
def log_required(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        if session.get('logged_in'):
            return fn(*args, **kwargs)
        return redirect(url_for('.login', next=request.path))
    return inner

@main.route("/draft/")
@log_required
def drafts():
    query = Entry.drafts().order_by(Entry.timestamp.desc())
    return objects_list('index.html', query)



@main.route('/create/', methods=['GET', 'POST'])
@log_required
def create():
    if request.method == 'POST':
        if request.form.get('title') and request.form.get('content'):
            entry = Entry.create(
                title=request.form['title'],
                content=request.form['content'],
                published=request.form.get('published') or False)
            flash('Entry created successfully.', 'success')
            if entry.published:
                return redirect(url_for('.detail', slug=entry.slug))
            else:
                return redirect(url_for('.edit', slug=entry.slug))
        else:
            flash('Title and Content are required.', 'danger')
    return render_template('create.html')



@main.route('/<slug>/edit/', methods=['GET', 'POST'])
@log_required
def edit(slug):
    entry = get_object_or_404(Entry, Entry.slug == slug)
    if request.method == 'POST':
        if request.form.get('title') and request.form.get('content'):
            entry.title = request.form['title']
            entry.content = request.form['content']
            entry.published = request.form.get('published') or False
            entry.save()

            flash('Entry saved successfully.', 'success')
            if entry.published:
                return redirect(url_for('.detail', slug=entry.slug))
            else:
                return redirect(url_for('.edit', slug=entry.slug))
        else:
            flash('Title and Content are required.', 'danger')

    return render_template('edit.html', entry=entry)



@main.route("/slug/")
def detail(slug):
    if session.get('logged_in'):
        query = Entry.select()
    else:
        query = Entry.public()
    entry = get_object_or_404(query, Entry.slug == slug)
    return render_template('detail.html', entry = entry)



@main.route('/')
def index():
    search_query = request.args.get('q')
    if search_query:
        query = Entry.search(search_query)
    else:
        query = Entry.public().order_by(Entry.timestamp.desc())
    return render_template("index.html", query = query)
@property
def html_content(self):
    hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
    extras = ExtraExtension()
    markdown_content = markdown(self.content, extensions=[hilite, extras])
    oembed_content = parse_html(
        markdown_content,
        oembed_providers,
        urlize_all=True,
        maxwidth=main.config['SITE_WIDTH'])
    return Markup(oembed_content)


@main.route('/login/', methods=['GET', 'POST'])
def login():
    logger.debug("log in, need account")
    logger.debug(url_for('main.static', filename='css/blog.min.css'))
    next_url = request.args.get("next") or request.form.get("next")
    if request.method == 'POST' and request.form.get("password"):
        if request.form.get("password") == app.config['PASSWORD']:
            session['logged_in'] = True
            session.permanent = True
            flash('you are now logged in', 'success')
            return redirect(url_for('.index'))
        else:
            flash('incorrect password.', 'danger')
    return render_template('login.html', next_url = next_url)
@main.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('main.login'))
    return render_template('logout.html')

@main.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        pass
    return render_template('register.html')




