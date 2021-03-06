from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import datetime


## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()
# print(posts)

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

posts = db.session.query(BlogPost).all()


@app.route('/')
def get_all_posts():

    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = db.session.query(BlogPost).get(index)
    for blog_post in posts:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/edit-post/<int:post_id>', methods=['GET','POST'])
def edit_post(post_id):
    form = CreatePostForm()
    editing_post = db.session.query(BlogPost).get(post_id)
    edit_page = CreatePostForm(
        title=editing_post.title,
        subtitle=editing_post.subtitle,
        body=editing_post.body,
        author=editing_post.author,
        img_url=editing_post.img_url
    )
    if form.validate_on_submit():
        editing_post.title = edit_page.title.data
        editing_post.subtitle = edit_page.subtitle.data
        editing_post.body = edit_page.body.data
        editing_post.author = edit_page.author.data
        editing_post.img_url = edit_page.img_url.data
        db.session.commit()
        return redirect(url_for('show_post', index = post_id))
    return render_template("make-post.html", is_edit_page = True, form=edit_page)


@app.route('/new_post', methods=['GET'])
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        newpost = BlogPost(
            title = form.title.data,
            subtitle = form.subtitle.data,
            date = datetime.datetime.now().strftime("%B %d, %Y"),
            body = form.body.data,
            author =form.author.data,
            img_url = form.img_url.data
        )
        db.session.add(newpost)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form = form)

@app.route('/delete/<int:post_id>', )
def delete_data(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(debug=True)

# host='0.0.0.0', port=5000