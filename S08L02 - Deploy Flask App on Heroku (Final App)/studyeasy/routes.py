import os
from PIL import Image
from flask import render_template, redirect, url_for, flash, request, abort
from studyeasy.forms import Register, Login, Account, PostForm
from studyeasy import app, bcrypt, db
from studyeasy.models import add_user, User, Post
from flask_login import login_required, login_user, logout_user, current_user



@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(per_page = 4, page=page)
    return render_template('home.html', title='Homepage', posts= posts)
    

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = Register()
    if form.validate_on_submit():
        add_user(form)
        flash('Registeration successful!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route('/add_post', methods=['POST', 'GET'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post added successfully', 'success')
        return redirect(url_for('home'))
    return render_template('add_update_post_form.html', title='Add post', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = Login()
    if form.validate_on_submit():
        result = User.query.filter_by(email=form.email.data).first()
        if result and bcrypt.check_password_hash(result.password, form.password.data):
            login_user(result,  remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect('home')
    else:
         return redirect('login')

def save_profile_pic(picture):
    filename = picture.filename
    _name, _ext = os.path.splitext(filename)
    new_name = bcrypt.generate_password_hash(_name).decode('utf-8')
    new_name = new_name[0:45] + _ext

    size = 128, 128

    im = Image.open(picture)
    im.thumbnail(size)
    _path = os.path.join(app.root_path, 'static/media/profile_pics', new_name)
    im.save(_path)
    return new_name

@app.route("/account", methods=['POST', 'GET'])
@login_required
def account():
    form = Account()
    if request.method == 'GET':
        form.name.data = current_user.name
        form.age.data = current_user.age
        form.email.data = current_user.email
        #form.profile_pic.data = current_user.profile_pic # No Need
    elif form.validate_on_submit():
        current_user.name = form.name.data
        current_user.age = form.age.data
        current_user.email = form.email.data
        if form.profile_pic.data:
            filename = save_profile_pic(form.profile_pic.data)
            current_user.profile_pic = filename
        db.session.commit()
        flash('Your account details have been updated', 'success')
        return redirect(url_for('account'))
   
    
    return render_template('account.html', title='Account', form=form)

@app.route("/post/<int:post_id>")
@login_required
def read_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('show_post.html', title=post.title, post=post)

@app.route("/post/update/<int:post_id>", methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    elif request.method == 'POST':
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('The article had been updated', 'success')
        return redirect(url_for('read_post', post_id= post_id))
    return render_template('add_update_post_form.html', title=post.title,form=form)

@app.route("/post/delete/<int:post_id>", methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('The article had been deleted', 'success')
    return redirect(url_for('home'))
    
