from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, session

from app.profile.forms import ChangePassForm, EditProfileForm, AddBudgetForm
from ..models import Product, User
from .. import db
from hashlib import md5
from flask_login import login_required, current_user
from . import profile
from ..email import send_email, send_congrat_email

@profile.route('/<username>')
def profile_page(username):
    if username is not None:        
        user = User.query.filter_by(user_name = username).first_or_404()
        email= user.user_email
        email_hash = md5(email.encode("utf-8")).hexdigest()
        if user.user_score > 5000:
            user_avatar = f"https://www.gravatar.com/avatar/{email_hash}?s=100&d=https://static.wikia.nocookie.net/leagueoflegends/images/2/29/Season_2019_-_Challenger_2.png/revision/latest/scale-to-width-down/250?cb=20181229234915"
        elif user.user_score > 2500:
            user_avatar = f"https://www.gravatar.com/avatar/{email_hash}?s=100&d=https://static.wikia.nocookie.net/leagueoflegends/images/a/a3/Season_2019_-_Platinum_2.png/revision/latest/scale-to-width-down/250?cb=20181229234933"
        else:        
            user_avatar = f"https://www.gravatar.com/avatar/{email_hash}?s=100&d=https://static.wikia.nocookie.net/leagueoflegends/images/f/f4/Season_2019_-_Bronze_1.png/revision/latest/scale-to-width-down/250?cb=20181229234910"
        return render_template('profile/profile.html', user=user, user_avatar=user_avatar)

@profile.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    user = User.query.filter_by(user_name = current_user.user_name).first()
    if form.validate_on_submit():
        user.user_name = form.username.data
        user.user_fullname = form.fullname.data
        user.user_phone = form.phone.data
        user.bio = form.bio.data
        db.session.commit()
        flash('Update profile succeed !', category='success')
        return redirect(url_for('profile.profile_page', username=current_user.user_name))
    if form.errors != {}:       #if there are errors
        for error in form.errors.values():
            flash(f'{error}', category='danger')
    return render_template('profile/edit_profile.html', user=user, form=form)

@profile.route('/add_budget', methods=['GET', 'POST'])
@login_required
def add_budget():
    form = AddBudgetForm()
    user = User.query.filter_by(user_name = current_user.user_name).first()
    if form.validate_on_submit():
        if (form.amount.data.isnumeric() == False):
            flash('Please enter a number !!', category='danger')
        else:
            token = user.generate_confirmation_token()          
            send_email(user.user_email, 'mail/add_budget', user=user, token=token, amount=form.amount.data)
            # user.user_budget += int(form.amount.data)
            # db.session.commit()
            flash('We just sent an email for you to confirm your transaction !', category='success')
    return render_template('profile/add_budget.html', user=user, form=form)
    
@profile.route('/confirm_add_budget/<amount>/<token>')
@login_required
def confirm_add_budget(amount,token):
    if current_user.confirm(token) == 'TRUE':
        current_user.user_budget += int(amount)
        db.session.commit()
    elif current_user.confirm(token) == 'TOUCHED':
        flash('The confirmation link is invalid. ', category='danger')
    elif current_user.confirm(token) == 'EXPIRED':
        flash('The confirmation link is expired. ', category='danger')
    else:
        flash('Something went wrong. ', category='danger')
    return redirect(url_for('main.home_page'))



@profile.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password() :
    form = ChangePassForm()
    if form.validate_on_submit():
        user = current_user
        if user is not None and user.check_password(form.old_password.data):
            user.password = form.new_password.data
            db.session.commit()
            flash('Password changed succeed.', category='success')
            return redirect(url_for('main.home_page'))
        flash('Wrong password!.', category='info')
    return render_template('profile/change_password.html', form=form)