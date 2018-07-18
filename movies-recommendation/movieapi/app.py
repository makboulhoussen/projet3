#! /usr/bin/env python
from flask import Flask, jsonify, abort
from . import moviedata
import logging as lg

app = Flask(__name__)


# On définit la route selon la structure de la requête demandée pour le projet
# On récupère les recommandations de films et on retourne une réponse de type JSON
@app.route('/recommend/<int:movie_id>', methods=['GET'])
def get_recommendation(movie_id):
	recommendations = moviedata.getMovieRecommendation(movie_id,5)
	if len(recommendations) == 0:
		abort(404)
	lg.warning("Recommendation based on movie : " + moviedata.getMovieTitleFromId(movie_id))
	return jsonify({'_results': recommendations})


if __name__ == '__main__':
    app.run()