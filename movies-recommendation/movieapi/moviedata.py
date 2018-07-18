import pandas as pd
import numpy as np
import logging as lg
from sklearn.metrics.pairwise import euclidean_distances
import json

# MovieData va contenir toutes les méthodes nécessaires à faire des recommendations de films à partir de nos données
# stockées dans les fichiers
# On se base sur le 1er fichier contenant la base de données des films nettoyées
# L'autre fichier contient les données vectorisées, standardisées et sur lesquelles on a fait une réduction de dimensions


movies_data=pd.DataFrame()
trans_movies_data=pd.DataFrame()

## METHODES


# Chargement des 2 fichiers de données
def init(data_file_path, transdata_file_path) :
    global movies_data, trans_movies_data
    movies_data = pd.read_csv(data_file_path)
    lg.warning("datafile " + data_file_path + " loaded.")
    trans_movies_data = np.load(transdata_file_path)
    lg.warning("datafile " + transdata_file_path + " loaded.")


# Retourne la position du film dans le dataset à partir de son ID
def getMoviePositionFromId(movie_id):
    m=movies_data.loc[movies_data['index_label'] == movie_id]
    return movies_data.index.get_loc(m.index.values.astype(int)[0])

# Retourne l'ID du film dans le dataset à partir de son index de position
def getMovieIdFromPosition(pos):
    return movies_data.iloc[pos]['index_label']

# Retourne l'index de position du film dans le dataset à partir du nom du film
def getMovieIdFromTitle(title) :
    m = movies_data.loc[movies_data['movie_title'] == title]
    return m.index_label.item()


# Retourne le nom du film à partir de son index de position dans le dataset 
def getMovieTitleFromPosition(pos):
    return movies_data.iloc[pos]['movie_title']

# Retourne le nom du film à partir de son ID dans le dataset 
def getMovieTitleFromId(movie_id):
    m = movies_data.loc[movies_data['index_label'] == movie_id]
    return m.movie_title.item()



# Retourne une liste des k films les plus proches du film identifié par son ID
def getShortedDistancesMovies(movie_id,k):
    pos = getMoviePositionFromId(movie_id)
    row_to_search = np.array(trans_movies_data[pos])
    distances=euclidean_distances(trans_movies_data, [row_to_search])
    closest = distances.argsort(axis=0)[:k+1].flatten()
    # on supprime le film lui même (il est le plus proche de lui même)
    closest=np.delete(closest, 0)
    movies = movies_data.iloc[closest]
    return movies


# Retourne une liste de n films recommendés pour l'utilisateur à partir de l'id du film donné
# La liste contient l'id et le nom des films
def getMovieRecommendation(movie_id, n) :
    recommendations=[]
    try :
        r_movies = getShortedDistancesMovies(movie_id, n)
        for index, row in r_movies.iterrows():
            d = {}
            d['id'] = int(getMovieIdFromPosition(index))
            d['name'] = str(row['movie_title']).strip()
            recommendations.append(d)
    except :
        lg.error("cannot find movie with ID :" + str(movie_id))
    return recommendations
