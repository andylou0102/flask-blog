from flask import (Blueprint, render_template, url_for,
                    flash, redirect, request, abort) 
from blog.posts.forms import PostForm
from blog import db
from blog.model import Post
from flask_login import current_user, login_required
from flask_mail import Message

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, subtitle=form.subtitle.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('貼文已成功發出', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', form = form, legend = 'New Post', title = 'New Post')

@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post = post, title = post.title)

@posts.route('/post/<int:post_id>/update', methods = ['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.content = form.content.data
        post.update_posted = datetime.utcnow()
        db.session.commit()
        flash('貼文更新完成', 'success')
        return redirect(url_for('posts.post', post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.subtitle.data = post.subtitle
        form.content.data = post.content
    return render_template('create_post.html', form = form, legend = 'Update', title = 'Update Post')

@posts.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('已刪除該貼文', 'success')
    return redirect(url_for('main.home'))
