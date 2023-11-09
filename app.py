from flask import Flask, request, render_template
import requests
app = Flask(__name__)

@app.route('/')
def homePage():
    return 'Welcome to the Pokemon Finder!'


@app.route('/pokeForm', methods=['GET','POST'])
def poke_form():
    if request.method =='POST':
        pokemon_data = request.form.get('pokemon_data')
        try:
            pokemon_url= f"https://pokeapi.co/api/v2/pokemon/{pokemon_data}"
            response = requests.get(pokemon_url)
            poke_stats = response.json()
            poke_dict = {
                'name' : poke_stats['forms'][0]['name'],
                'ability_name' : poke_stats['abilities'][1]['ability']['name'],
                'base_experience' : poke_stats['base_experience'],
                'attack_base_stat' : poke_stats['stats'][1]['base_stat'],
                'defense_base_stat' : poke_stats['stats'][2]['base_stat'],
                'hp_base_stat' : poke_stats['stats'][0]['base_stat'],
                'sprites_image': poke_stats['sprites']['front_shiny']
            }
           
            return render_template('pokeForm.html', pokemon_info=poke_dict)
        except:
            return render_template('pokeForm.html')
    else:
        return render_template('pokeForm.html')