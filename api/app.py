from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)

#Methode GET
@app.route('/get_film/<int:film_id>', methods=['GET'])
def get_film(film_id):
    with open('videotheque.json', 'r') as file:
        videotheque = json.load(file)
    for film in videotheque:
        if film['id'] == film_id:
            return jsonify(film)
    return jsonify({'message': f'Auncun film trouvé avec cet ID {film_id}'}), 404

@app.route("/films", methods=['GET'])
def get_films():
    with open('videotheque.json', 'r') as file:
        videotheque = json.load(file)
    return jsonify({'Films' : videotheque})


# Méthode GET pour récupérer un film par son titre
"""@app.route('/get_film_titre/<string:titre>', methods=['GET'])
def get_film_titre(film_titre):
    with open('videotheque.json', 'r') as file:
        videotheque = json.load(file)

    for film in videotheque:
        if film['titre'].lower() == film_titre.lower():
            return jsonify(film) 
    return jsonify({'message': f'Aucun film trouvé avec le titre "{film_titre}"'}), 404"""

"""@app.route('/rechercher_par_titre/<string:titre>', methods=['GET'])
def rechercher_par_titre(titre):
    with open('videotheque.json', 'r') as file:
        videotheque = json.load(file)

    films_recherches = [film for film in videotheque if film['titre'].lower() == titre.lower()]

    #return jsonify({'Films': films_recherches})
    return jsonify(films_recherches) """

#Methode PUT
@app.route("/update_films/<int:film_id>", methods=['PUT'])
def update_film(film_id):
    with open('videotheque.json', 'r') as file:
        videotheque = json.load(file)

    for film in videotheque:
        if film['id'] == film_id:
            film['titre'] = request.json.get('titre', film['titre'])
            film['realisateur'] = request.json.get('realisateur', film['realisateur'])
            film['annee_sortie'] = request.json.get('annee_sortie', film['annee_sortie'])
            film['genre'] = request.json.get('genre', film['genre'])
            film['acteurs'] = request.json.get('acteurs', film['acteurs'])
            film['duree'] = request.json.get('duree', film['duree'])
            film['synopsis'] = request.json.get('synopsis', film['synopsis'])
            film['image'] = request.json.get('image', film['image'])

            # Enregistrer les modifications dans le fichier JSON
            with open('videotheque.json', 'w') as file:
                json.dump(videotheque, file, indent=2)
            return jsonify({'message': f'Film avec ID {film_id} modifié avec succès'})

    return jsonify({'message': f'Aucun film trouvé avec l\'ID {film_id}'}), 404

# Méthode POST pour ajouter un film
@app.route("/ajout_films", methods=['POST'])
def add_film():
    new_film = {
        'id': request.json.get('id'),
        'titre': request.json.get('titre'),
        'realisateur': request.json.get('realisateur'),
        'annee_sortie': request.json.get('annee_sortie'),
        'genre': request.json.get('genre'),
        'acteurs': request.json.get('acteurs'),
        'duree': request.json.get('duree'),
        'synopsis': request.json.get('synopsis'),
        'image': request.json.get('image'),
    }
    with open('videotheque.json', 'r') as file:
        videotheque = json.load(file)
    videotheque.append(new_film)
    with open('videotheque.json', 'w') as file:
        json.dump(videotheque, file, indent=2)

    return jsonify({'message': 'Film ajouté avec succès'})

# Méthode DELETE pour supprimer un film
@app.route("/delete_films/<int:film_id>", methods=['DELETE'])
def delete_film(film_id):
    with open('videotheque.json', 'r') as file:
        videotheque = json.load(file)

    updated_videotheque = [film for film in videotheque if film['id'] != film_id]

    if len(updated_videotheque) < len(videotheque):
        with open('videotheque.json', 'w') as file:
            json.dump(updated_videotheque, file, indent=2)

        return jsonify({'message': f'Film avec ID {film_id} supprimé avec succès'})

    return jsonify({'message': f'Aucun film trouvé avec l\'ID {film_id}'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)