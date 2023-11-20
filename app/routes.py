from flask import request, render_template, redirect, url_for, flash
import requests
from app import app
from app.forms import pokeFormForm, LoginForm, SignupForm
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

# Home
@app.route('/')
@app.route('/home')
def homePage():
    return render_template('home.html')

# poke form
@app.route('/pokeForm', methods=['GET','POST'])
def poke_form():
    form = pokeFormForm()
    if request.method =='POST':
        poke_data = form.name.data
        try:
            print(poke_data)
            poke_url= f"https://pokeapi.co/api/v2/pokemon/{poke_data}"
            response = requests.get(poke_url)
            poke_stats = response.json()
            poke_dict = {
                'name' : poke_stats['forms'][0]['name'],
                'ability_name' :poke_stats['abilities'][1]['ability']['name'],
                'base_experience' :poke_stats['base_experience'],
                'attack_base_stat' :poke_stats['stats'][1]['base_stat'],
                'defense_base_stat' :poke_stats['stats'][2]['base_stat'],
                'hp_base_stat' :poke_stats['stats'][0]['base_stat'],
                'sprites_image':poke_stats['sprites']['front_shiny']
            }
           
            return render_template('pokeForm.html', pokemon_info=poke_dict, form=form)
        except:
            return render_template('pokeForm.html',form=form)
    else:
        return render_template('pokeForm.html', form=form)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() 
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Hello, {queried_user.first_name}!', 'success')
            return redirect(url_for('homePage'))
        else:
            return 'Invalid email or password'
    else:
        return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        firstName = form.firstName.data
        lastName = form.lastName.data
        email = form.email.data
        password = form.password.data

        user = User(firstName, lastName, email, password)

        db.session.add(user)
        db.session.commit()

        flash(f'Thank you for signing up {firstName}!', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)
    
@app.route ('/logout')
@login_required
def logout():
        flash('Successfully logged out', 'warning')
        logout_user()
        return redirect(url_for('login'))