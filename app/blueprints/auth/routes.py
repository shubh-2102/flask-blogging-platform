from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from app.blueprints.auth import auth_bp
from app.blueprints.auth.forms import RegistrationForm, LoginForm, EditProfileForm
from app.extensions import db
from app.models.user import User


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower()
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {user.username}! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form, title='Create Account')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome back, {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('auth/login.html', form=form, title='Sign In')


@auth_bp.route('/logout')
@login_required
def logout():
    flash(f'Goodbye, {current_user.username}! You have been logged out.', 'info')
    logout_user()
    return redirect(url_for('main.index'))


@auth_bp.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.filter_by(published=True).order_by(
        db.text('created_at DESC')
    ).paginate(page=page, per_page=6, error_out=False)
    total_posts = user.posts.filter_by(published=True).count()
    return render_template('auth/profile.html', user=user, posts=posts, total_posts=total_posts, title=f'{user.username}\'s Profile')


@auth_bp.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.bio = form.bio.data.strip()
        current_user.avatar_url = form.avatar_url.data.strip()
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('auth.profile', username=current_user.username))

    return render_template('auth/edit_profile.html', form=form, title='Edit Profile')
