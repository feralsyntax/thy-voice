from flask import abort, redirect, render_template, url_for
from flask_login import current_user, login_required

from .. import db
from ..email import mail_message
from ..models import Blog, Comment, User
from ..requests import get_quotes
from . import main
from .forms import (
    BlogForm,
    CommentForm,
    DeleteBlog,
    DeleteComment,
    SubscriptionForm,
    UpdateBlog,
    UpdateProfile,
)


# views
@main.route("/", methods=["GET", "POST"])
def index():
    """
    :return: index page + data
    """

    title = "ThyVoice- Welcome!"

    # blogs = Blog.query.all()
    blogs = db.session.query(Blog).order_by(Blog.blog_title.desc())

    my_quotes = get_quotes()

    print(my_quotes)

    return render_template("index.html", title=title, blogs=blogs, my_quotes=my_quotes)


@main.route("/user/<uname>/")
@login_required
def profile(uname):

    user = User.query.filter_by(username=uname).first()
    user_id = current_user._get_current_object().id
    user_blogs = Blog.query.filter_by(user_id=user_id).all()

    if user is None:
        abort(404)

    return render_template(
        "profile/profile.html",
        user=user,
        user_blogs=user_blogs,
        user_id=user_id,
        blog=blog,
    )


@main.route("/user/<uname>/update", methods=["GET", "POST"])
@login_required
def update_profile(uname):

    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    update_form = UpdateProfile()

    if update_form.validate_on_submit():
        user.bio = update_form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for(".profile", uname=user.username))

    return render_template("profile/update.html", user=user, update_form=update_form)


@main.route("/user/<uname>/<id>/update_blog", methods=["GET", "POST"])
@login_required
def update_blog(uname, id):

    user = User.query.filter_by(username=uname).first()
    # user_id = current_user._get_current_object().id
    # user_blog = Blog.query.filter_by(user_id=user_id).first()

    blog = Blog.query.get(id)

    if blog is None:
        abort(404)

    update_blog = UpdateBlog()

    if update_blog.validate_on_submit():
        blog.blog_title = update_blog.new_blog_title.data
        blog.blog_content = update_blog.new_blog_content.data
        blog.blog_category = update_blog.new_blog_category.data

        db.session.add(blog)
        db.session.commit()

        return redirect(url_for(".profile", uname=user.username))

    return render_template(
        "profile/update_blog.html",
        user=user,
        update_blog=update_blog,
        delete_blog=delete_blog,
        blog=blog,
    )


@main.route("/user/<uname>/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete_blog(uname, id):

    user = User.query.filter_by(username=uname).first()

    blog = Blog.query.get(id)

    if blog is None:
        abort(404)

    delete_blog = DeleteBlog()

    if delete_blog.validate_on_submit():
        db.session.delete(blog)
        db.session.commit()

        return redirect(url_for(".profile", uname=user.username))

    return render_template(
        "profile/delete.html", user=user, delete_blog=delete_blog, blog=blog
    )


@main.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """
    :return: index page + data
    """

    blogs = Blog.query.all()
    blog_form = BlogForm()

    if blog_form.validate_on_submit():
        blog_title = blog_form.blog_title.data
        blog_category = blog_form.blog_category.data
        blog_description = blog_form.blog_description.data
        blog_content = blog_form.blog_content.data
        user_id = current_user._get_current_object().id

        new_blog_dict = Blog(
            blog_title=blog_title,
            user_id=user_id,
            blog_category=blog_category,
            blog_content=blog_content,
            blog_description=blog_description,
        )

        new_blog_dict.save_blog()

        return redirect(url_for("main.index"))

    title = "Create Blog- ThyVoice!"

    return render_template(
        "create.html", title=title, blogs=blogs, blog_form=blog_form, blog=blog
    )


# @main.route('/create/<filename>/pic')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'],filename)
#


@main.route("/subscribe", methods=["GET", "POST"])
def subscribe():
    subscription_form = SubscriptionForm()

    if subscription_form.validate_on_submit():
        user = User(email=subscription_form.email.data)

        mail_message("Your Subscription", "email/subscribe_user", user.email, user=user)

        return redirect(url_for(".index"))

    title = "Subscription"

    return render_template(
        "subscribe.html", subscription_form=subscription_form, title=title
    )


@main.route("/blog/<int:id>", methods=["GET", "POST"])
@login_required
def blog(id):
    """
    :return: blog feed page + data
    """

    blog = Blog.query.get(id)
    comment_form = CommentForm()
    comments = Comment.query.all()
    comment = Comment.query.get(id)

    user = current_user._get_current_object().username
    # blog_id = Blog.query.get(id)
    # blog = Blog.query.filter_by(blog_id=blog_id).first()

    if user is None:
        abort(404)

    if comment_form.validate_on_submit():
        blog = Blog.query.get(id)
        comment_message = comment_form.comment.data
        comment = Comment(comment_message=comment_message)

        db.session.add(comment)
        db.session.commit()

        return redirect(url_for(".blog", id=blog.id))

    title = "Blog"

    return render_template(
        "blog.html",
        title=title,
        blog=blog,
        comment=comment,
        comment_form=comment_form,
        comments=comments,
    )


@main.route("/blog/<int:id>/update", methods=["GET", "POST"])
@login_required
def delete_comment(id):

    comment = Comment.query.get(id)
    blog = Blog.query.get(id)

    if comment is None:
        abort(404)

    delete_comment = DeleteComment()

    if delete_comment.validate_on_submit():
        db.session.delete(comment)
        db.session.commit()

        return redirect(url_for(".blog", id=blog.id))

    return render_template(
        "delete_comment.html", delete_comment=delete_comment, blog=blog
    )
