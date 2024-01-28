from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
import os
import json
import requests
import http.client

#app = Flask(__name__)
#app = Flask(__name__, static_url_path='/static')
app = Flask(__name__, template_folder='templates')

static_dir = os.path.abspath('static')
app.static_folder = static_dir
app.static_url_path = '/static'

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#POUR Afficher les FILMs dans index
def api_request2():
    url = "http://172.19.0.10:5000/films"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch data. Status code: {e}")

@app.route('/')
def index():   
    try:        
        #data = api_request1()
        data = api_request2()
        videotheques =[]

        for videotheque_data in data.get("Films", []):
            Films= {
                'id': videotheque_data.get('id'),
                'titre': videotheque_data.get('titre'),
                'realisateur': videotheque_data.get('realisateur'),                
                'annee_sortie': videotheque_data.get('annee_sortie'),
                'genre': videotheque_data.get('genre'),
                'acteurs': videotheque_data.get('acteurs'),
                'duree': videotheque_data.get('duree'),
                'synopsis': videotheque_data.get('synopsis'),
                'image': videotheque_data.get('image'),
            }
            videotheques.append(Films)
        return render_template("index.html", videotheques=videotheques)
    except Exception as e:
        print(f"An error occured: {e}") 
        return jsonify({"error": str(e)})


#Pour ajouter un film
def api_ajouter_film(nouveau_film):
    url = "http://172.19.0.10:5000/ajout_films"
    #url = "{{ url_for('/ajout_films)}}"
    try:
        response = requests.post(url, json=nouveau_film)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failes to add film. Error: {e}")

@app.route('/ajout_films', methods=['GET'])
def lire_films():
    #return render_template("ajouter_film.html")
    return render_template("ajouterr_film.html")

@app.route('/ajout_films', methods=['POST'])
def ajout_films():
    if request.method == 'POST':
        try:
            film_id = int(request.form['id'])
            nouveau_film = {
                'id': request.form['id'],
                'titre': request.form['titre'],
                'realisateur': request.form['realisateur'],
                'annee_sortie': request.form['annee_sortie'],
                'genre': request.form['genre'].split(','),
                'acteurs': request.form['acteurs'].split(','),
                'duree': request.form['duree'],
                'image': request.form['image'],
                'synopsis': request.form['synopsis'],
            }
            api_ajouter_film(nouveau_film)

            flash('Film ajouté avec succes', 'success')
            return redirect(url_for("index"))

        except Exception as e:
            flash(f"Echec d'ajout du film. Erreur : {e}", 'error')
    #return render_template("ajouter_film.html")
    return render_template("ajouterr_film.html")


#Pour supprimer un film
def api_delete_film(film_id):
    delete_url = f"http://172.19.0.10:5000/delete_films/{film_id}"
    try:
        response = requests.delete(delete_url)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to delete the film. Status code: {e}")

@app.route('/delete_films/<int:film_id>', methods=['POST', 'DELETE'])
def delete_film(film_id):
    try:
        success = api_delete_film(film_id)

        if success:
            flash('Film deleted successfully', 'success')
        else:
            flash('Failed to delete the film', 'error')

        return redirect(url_for('index'))
    except Exception as e:
        print(f"An error occurred: {e}")
        flash('An error occurred while deleting the film', 'error')
        #return redirect(url_for('index'))
        return jsonify({"error": str(e)})


def api_get_film(film_id):
    #url = f"http://172.19.0.10:5000/get_film/{film_id}"
    try:
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        response = requests.get(f"http://172.19.0.10:5000/get_film/{film_id}", headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except ValueError:
        raise Exception("Invalid film_id format.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch film. Error: {e}")

#Route Pour afficher les details d'un film
@app.route('/modifier_films/<int:film_id>', methods=['GET'])
def modifier_films(film_id):
    try:
        film_details = api_get_film(film_id)
        return render_template("modifier_films.html", film_details=film_details)
    except Exception as e:
        flash(f"Failed to fetch film details Error : {e}", 'error')
        return redirect(url_for('index'))

#Fonction pour mettre a jour un film par id
def api_update_film(film_id, updated_film):   
    try:
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        url = f"http://172.19.0.10:5000/update_films/{film_id}"
        response = requests.put(url, json=updated_film, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except ValueError:
        raise Exception("Invalid film_id format.")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch film. Error: {e}") 
    
#Route pour mettre a jour le film
@app.route('/update_films/<int:film_id>', methods=['GET', 'POST'])
def update_films(film_id):
    film_details = None   
    if request.method == 'POST':        
        try:      
            #film_details = api_get_film(film_id)
            film_details = None  
            updated_film = {
                'id': film_id,
                'titre': request.form['titre'],
                'realisateur': request.form['realisateur'],
                'annee_sortie': request.form['annee_sortie'],
                'genre': request.form['genre'].split(','),
                'acteurs': request.form['acteurs'].split(','),
                'duree': request.form['duree'],
                'image': request.form['image'],
                'synopsis': request.form['synopsis'],
            }
            api_update_film(film_id, updated_film)

            flash('Film mis à jour avec succès', 'success')
            return redirect(url_for("index"))
            #return redirect(url_for("modifier_films", film_id=film_id))
        
        except ValueError as e:
            flash(f"Erreur de mise à jour du films: {e}", 'error')
            return redirect(url_for('modifier_films', film_id=film_id))

        except Exception as e:
            flash(f"Echec de la mise à jour du film. Erreur : {e}", 'error')
            return redirect(url_for('modifier_films', film_id=film_id))
    film_details = api_get_film(film_id)
    if film_details is not None:
        return render_template("modifier_films.html", film_details=film_details)
    else:
        flash('Film non trouve', 'error')
        return redirect(url_for('index'))

# Fonction pour effectuer la recherche par titre
"""def api_rechercher_par_titre(titre):
    url = f"http://172.19.0.10:5000/rechercher_par_titre/{titre}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"Échec de la recherche par titre. Erreur : {e}")
"""
# Méthode GET pour rechercher des films par titre
"""@app.route('/rechercher_par_titre/<string:titre>', methods=['GET'])
def rechercher_par_titre(titre):
    with open('videotheque.json', 'r') as file:
        videotheque = json.load(file)

    films_recherches = [film for film in videotheque if film.get('titre', '').lower() == titre.lower()]

    return jsonify(films_recherches)"""


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=8000)

