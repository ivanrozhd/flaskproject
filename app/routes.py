from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt_
from app.models import User, Interests
from app.forms import RegistrationForm, LoginForm, InterestForm
from flask import session


main = Blueprint('main', __name__)

@main.route("/")
def home():
    """
    Home page
    :return:
    """

    return render_template('home.html')

@main.route("/register", methods=["POST","GET"])
def register():

    """
    Registers the user
    :return: redirect to login page
    """
    if current_user.is_authenticated:
        session.pop('_flashes', None)
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if request.method == "POST":
        session.pop('_flashes', None)
        if form.validate_on_submit():
            hashed_password = bcrypt_.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.login'))
        else:
            flash('Passwords do not match each other!!!', 'danger')
            return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)


@main.route("/login", methods=["POST","GET"])
def login():

    """
    Logs in the user
    :return:
    """

    if current_user.is_authenticated:
        return redirect(url_for('main.mypage', username=current_user.username))
    form = LoginForm()
    if request.method == "POST":
        session.pop('_flashes', None)
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt_.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('main.mypage',  username=user.username))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
                return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)


@main.route("/mypage/<username>", methods=["POST","GET"])
@login_required
def mypage(username):

    """
    :param username: current user
    :return:
    """

    user = User.query.filter_by(username=username).first_or_404()
    form = InterestForm()
    if form.validate_on_submit():
        new_interest = Interests(hobby=form.hobby.data, description=form.description.data, user_id=user.id)
        db.session.add(new_interest)
        db.session.commit()
        flash('Interest added successfully!', 'success')
        return redirect(url_for('main.mypage', username=username))
    else:
        print(form.errors)
    interests = Interests.query.filter_by(user_id=user.id).all()
    print(f"Raw Query Result: {Interests.query.filter_by(user_id=user.id).all()}")

    return render_template('mypage.html', user=user, form=form, interests=interests)


@main.route("/mypage/<username>/delete")
def delete_all(username):
    """
    :param username: current user
    :return: redirect to home page
    """
    user = User.query.filter_by(username=username).delete()
    db.session.commit()
    flash('Account deleted successfully!', 'success')
    return redirect(url_for('main.home'))



@main.route("/mypage/<username>/delete/<int:id>")
def delete(username, id):
    """
    :param username: current user
    :param id: id of the interest to be deleted
    :return: redirect to mypage

    """

    if current_user.username != username:
        flash("You are not authorized to delete this interest.", "danger")
        return redirect(url_for('main.mypage', username=current_user.username))

    interest = Interests.query.get_or_404(id)
    if interest.user_id != current_user.id:
        flash("You are not authorized to delete this interest.", "danger")
        return redirect(url_for('main.mypage', username=current_user.username))

    db.session.delete(interest)
    db.session.commit()
    flash('Interest deleted successfully!', 'success')

    return redirect(url_for('main.mypage', username=username))


@main.route("/mypage/<username>/update/<int:id>", methods=["POST", "GET"])
@login_required
def update_interest(username, id):
    # Ensure the interest belongs to the current user
    interest = Interests.query.get_or_404(id)
    form = InterestForm()
    if interest.user_id != current_user.id:
        flash("You are not authorized to update this interest.", "danger")
        return redirect(url_for('main.mypage', username=username))


    if request.method == "POST":
        # Get data from the form
        new_hobby = request.form.get('hobby')
        new_description = request.form.get('description')

        # Update the interest
        if new_hobby:
            interest.hobby = new_hobby
        if new_description:
            interest.description = new_description

        # Save changes
        db.session.commit()
        flash("Interest updated successfully!", "success")
        return redirect(url_for('main.mypage', username=username))

    return render_template('update.html',interest=interest, form=form)





@main.route("/logout")
def logout():

    """
    Logs out the current user
    :return: redirect to home page
    """
    logout_user()
    return redirect(url_for('main.home'))






