from sqlite3 import IntegrityError
from flask import render_template, redirect, url_for, flash,request, abort,Blueprint
import sqlalchemy
from flasktasks import app , forms,db, bcrypt , login_manager
from flasktasks.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
from flasktasks.forms import PostForm
from flask_sqlalchemy import Pagination




nav_items = [
    {'name': 'Home', 'url': '/home'},
    {'name': 'About', 'url': '/about'},
    {'name': 'Register', 'url': '/register'},
    {'name': 'Login', 'url': '/login'}


]
users = [
    {'email': 'test@example.com',
     'password1':'12345678',
      },
     {'email': 'test2@example.com',
     'password1':'12345678',
      },
]


    

@app.route('/home')
@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Number of posts per page
    posts = Post.query.paginate(page=page, per_page=per_page)
    return render_template('home.html', nav_items=nav_items, posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', nav_items=nav_items)

@app.route('/register' , methods=['POST','GET'])
def register():
    register_form = forms.RegisterForm()
    if register_form.validate_on_submit():
        try:
                  with app.app_context():
                            hashed_pw = bcrypt.generate_password_hash(register_form.password1.data).decode('utf-8')
                            new_user = User(
                                name=register_form.name.data,
                                email=register_form.email.data,
                                password=hashed_pw
                            )
                            db.session.add(new_user)
                            db.session.commit()

                            flash(f"Registration Successful for {register_form.email.data}!")
                            return redirect(url_for('home'))
        except sqlalchemy.exc.IntegrityError:
                    flash(f"Email Already Exists!")
                    return redirect(url_for('register'))

                        
        
        
      
    return render_template('register.html', data = {'form': register_form , 'nav_items': nav_items})

@app.route('/login' , methods=['POST','GET'])
def login():
    flag = False
    login_form = forms.LoginForm()
    if login_form.validate_on_submit():
        with app.app_context():
            user = User.query.filter_by(email=login_form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, login_form.password.data):
                login_user(user)
                flash(f"Logging in Successful for {login_form.email.data}!")
                return redirect(url_for('home'))
            else:   
                    print("Login Failed")
                    flash(f"Invalid email or password")
                    return render_template('login.html', data = {'form': login_form , 'nav_items': nav_items})
                
    return render_template('login.html', data = {'form': login_form , 'nav_items': nav_items})


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ______________posts_______________
posts = Blueprint('posts', __name__)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

# _____users_______

# @users.route("/user/<string:username>")
# def user_posts(username):
#     page = request.args.get('page', 1, type=int)
#     user = User.query.filter_by(username=username).first_or_404()
#     posts = Post.query.filter_by(author=user)\
#         .order_by(Post.date_posted.desc())\
#         .paginate(page=page, per_page=5)
#     return render_template('user_posts.html', posts=posts, user=user)

