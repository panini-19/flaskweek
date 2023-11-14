from flask import request, render_template
import requests
from app import app
from app.forms import pokeFormForm
from app.forms import LoginForm
from app.forms import SignupForm

# Home
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
    
REGISTERED_USERS={
    "ani@pokemon.org":{
        "name": "Anthony Ni",
        "password":"panini19"
    }
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() 
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if email in REGISTERED_USERS and REGISTERED_USERS[email]['password'] == password:
            return f'Hello, {REGISTERED_USERS[email]["name"]}'
        else:
            return 'Invalid email or password'
    else:
        return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        full_name = f'{form.firstName.data} {form.lastName.data}'
        email = form.email.data
        password= form.password.data
        REGISTERED_USERS[email] ={
            'name':full_name,
            'password':password
        }
        return f'Welcome {full_name}, thank you for signing up!'
    else:
        return render_template('signup.html', form=form)