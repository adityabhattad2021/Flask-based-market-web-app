from Flask_Project import app
from flask import render_template, redirect, url_for, flash, request
from Flask_Project.models import Items, User
from Flask_Project.forms import RegisterForm, LoginForm, PurchaceItemForm, SellItemForm
from Flask_Project import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def hello_flask():
    return render_template('index.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaceItemForm()
    selling_form=SellItemForm()
    if request.method == "POST":
        # purchaced item logic.
        purchased_item = request.form.get('purchased_item')
        p_item_object = Items.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.assign_ownership(current_user)
                flash(f'You just purchased a {p_item_object.name} for ₹{p_item_object.price}.')
            else:
                flash("Unfortunately you don't have enough money to purchace {{p_item_object.name}}.")
        # Sold item logic.
        sold_item = request.form.get("sold_item")
        s_item_object=Items.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f'Coratulations you just sold {s_item_object} back to the market!')
            else:
                flash(f"Something went wrong, could not sell {s_item_object}!")

        return redirect(url_for('market_page'))
    if request.method == 'GET':
        items = Items.query.filter_by(owner=None)
        owned_items=Items.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form,owned_items=owned_items,selling_form=selling_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"User created successfully! You are now logged in as {user_to_create.username}.", category='success')
        return redirect(url_for('market_page'))
    # Check if there are no errors from the validations.
    if form.errors != {}:
        for err_msg in form.errors.values():
            # error_message=f'There was an error while creating the website: {err_msg}'
            flash(f'There was an error while creating the website: {err_msg}', category='danger')
            # print(f'There was an error while creating the website: {err_msg}')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Login successful, {attempted_user.username} ", category='success')
            return redirect(url_for('market_page'))
        else:
            flash("Either of username or password is incorrect", category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have logged out successfully!")
    return redirect(url_for('hello_flask'))
