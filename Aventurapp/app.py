from flask import Flask
from routes.routes_admin import *
from routes.routes_aventurapp import *


app = Flask(__name__)

routes_personalitzades(app)
routes_aventurers(app)
routes_continguts(app)
routes_estatiques(app)
routes_home(app)
routes_homes(app)
routes_inici(app)
routes_inici_subscripcions_aventurers(app)
routes_inici_subscripcions_ocasionals(app)
routes_inici_viatges(app)
routes_poblacions(app)
routes_personalitzades(app)
routes_llistes(app)
routes_users(app)
routes_ocasionals(app)


######################################################
# ADMINISTRACIÓ
######################################################


##################################
# ADMINISTRACIÓ
##################################

####################
# Aventurers
####################

####################
# Ocasionals
####################

####################################
## Poblacions
####################################

############
# Viatges
############

#######################
# Llistes
#######################

###############################
# Estatiques
###############################

###############################
# Personalitzades
###############################

##############################
## Continguts
##############################

##############################
## Subscripcions_aventurers
##############################


###########################
# Subscripcions_ocasionals
############################


##############################
## Aplicació Usuari
##############################



############
# Homes
############


############
# Viatges
############


############################
# Estatiques i subscripcions ocasionals
############################

###############################
# Creació llista personalitzada
###############################
