from .import main
from flask import (request, render_template, session, url_for, redirect, flash)
import functools
from test.log import logger, set_log
from playhouse.flask_utils import object_list, get_object_or_404
from APP.alchemy_model import Post

from APP.form import PostForm
from manage import APP

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
    query = Post.drafts().order_by(Entry.timestamp.desc())
    return objects_list('index.html', query)



@main.route('/create/', methods=['GET', 'POST'])
#@log_required
def create():
    post_form = PostForm()
    #check if method is 'POST' & data is validate
    if post_form.validate_on_submit():
        post = Post.insert(title=post_form.title.data,
                           content=post_form.content.data,
                           published=post_form.published.data
                          )
        flash('Post created successfully.', 'success')
        if post.published:
            return redirect(url_for('.detail', slug=post.slug))
        else:
            return redirect(url_for('.edit', slug=post.slug))
    return render_template('create.html', post_form=PostForm())



@main.route('/<slug>/edit/', methods=['GET', 'POST'])
#@log_required
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
    search_query = request.args.get('q')
    if search_query:
        query = Post.search(search_query)
    else:
        posts = Post.query_posts()
    return render_template("index.html", posts = posts)
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
        if request.form.get("password") == APP.config['PASSWORD']:
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
