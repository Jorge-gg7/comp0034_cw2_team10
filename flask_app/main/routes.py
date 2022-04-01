from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_required, logout_user
from flask_app.main.forms import PostForm
from flask_app import db
from flask_app.models import Post
from datetime import datetime

main_bp = Blueprint('main_bp', __name__)


@main_bp.route('/')
def home():
    if not current_user.is_anonymous:
        name = current_user.first_name
        flash(f'Hello {name}. ')
    posts = Post.query.all()
    return render_template('home.html', title='Home page', posts=posts)


@main_bp.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, date_posted=datetime.utcnow(), content=form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main_bp.home'))
    return render_template('create_post.html', title='New Post', form=form)
