from flask import Flask, render_template, request, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY']='aiguahojgu2y175861yg1h$'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newblog.db'

db = SQLAlchemy(app)
class Flags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(20))
    title = db.Column(db.String(50))
class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    number = db.Column(db.Text)
    content = db.Column(db.Text)
    comments = db.relationship('Comment', backref='blogpost', lazy=True)
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(60),nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('blogpost.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.body}', '{self.timestamp}')"
@app.route("/")
def home():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('index.html', posts=posts)
@app.route('/test/')
def test():
    return render_template('base.html')
@app.route('/post/<int:post_id>',methods=['GET','POST'])
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    comment = Comment.query.filter_by(post_id=post_id).all()
    if request.method == "POST":
        comment = Comment(body=request.form.get('title'), blogpost =post,author=request.form.get('author'))
        print(comment)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been added to the post", "success")
        return redirect(url_for("post",post_id=post_id))
    return render_template('post.html', post=post,comments=comment)
@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    number = request.form['number']

    post = Blogpost(title=title, subtitle=subtitle, number=number,author=author, content=content, date_posted=datetime.now())
    db.session.add(post)
    db.session.commit()
    flash("Posted Successfully!","success")
    return redirect(url_for('home'))
@app.route('/flag')
def flag():
    return render_template('flag.html')
@app.route('/flagproccess',methods=['POST','GET'])
def processflag():
    flag = Flags(author=request.form['author'],title=request.form['title'])
    db.session.add(flag)
    db.session.commit()
    flash('Flag Sent for Review!','success')
    return redirect(url_for('home'))
@app.route("/post/<int:post_id>/comment", methods=["GET", "POST"])
def comment_post(post_id):
    post = Blogpost.query.get_or_404(post_id)
    new_ = post.id
    if request.method =="POST":
        print(new_)
        comment = Comment(body=request.form.get('title'), blogpost =post,author=request.form.get('author'))
        print(comment)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been added to the post", "success")
        return redirect(url_for("home"))
    return render_template("comment.html")
@app.route('/post/<int:post_id>/comments/', methods=["GET", "POST"])
def view_comments(post_id):
    post = Blogpost.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id = post.id)
    return render_template('comments.html',comments=comments)
@app.route('/post/<int:post_id>/<int:comment_id>/', methods=["GET", "POST"])
def view_single_comment(post_id,comment_id):
    comments = Comment.query.filter_by(id = comment_id,post_id = post_id)
    return render_template('singlecomment.html',comment=comments[0])
