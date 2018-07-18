from flask import Flask
from .app import app
from . import moviedata
import logging as lg
from . import config

## VARIABLES
#'datafiles/movie_metadata_cleaned.csv'  
data_file_path=config.CLEAN_DATA_FILENAME

#'datafiles/movie_metadata_transformed.npy'
transdata_file_path=config.TRANSFORMED_DATA_FILENAME



log = lg.getLogger('werkzeug')
log.setLevel(lg.DEBUG)

moviedata.init(data_file_path, transdata_file_path)
   