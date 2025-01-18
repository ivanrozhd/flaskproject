from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt_
from app.models import User, Interests
from app.forms import RegistrationForm, LoginForm, InterestForm


main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template('home.html')

@main.route("/register", methods=["POST","GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            hashed_password = bcrypt_.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('main.login'))
    else:
        return render_template('register.html', form=form)


@main.route("/login", methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.mypage', username=current_user.username))
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt_.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('main.mypage',  username=user.username))
            else:
                flash('Login unsuccessful. Please check email and password.', 'danger')
    else:
        return render_template('login.html', form=form)


@main.route("/mypage/<username>", methods=["POST","GET"])
@login_required
def mypage(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = InterestForm()
    if form.validate_on_submit():
        print(f"Hobby: {form.hobby.data}, Description: {form.description.data}")
        new_interest = Interests(hobby=form.hobby.data, description=form.description.data, user_id=user.id)
        print(new_interest.hobby, " name of your hobby")
        db.session.add(new_interest)
        db.session.commit()
        flash('Interest added successfully!', 'success')
        return redirect(url_for('main.mypage', username=username))
    else:
        print(form.errors)
    interests = Interests.query.filter_by(user_id=user.id).all()
    print(f"Raw Query Result: {Interests.query.filter_by(user_id=user.id).all()}")

    return render_template('mypage.html', user=user, form=form, interests=interests)
    #return render_template('mypage.html', user=user, form=form)



@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))






