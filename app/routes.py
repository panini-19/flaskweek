from flask import request, render_template
import requests
from app import app
from app.forms import pokeFormForm

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