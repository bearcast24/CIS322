


# Write a script named preflight.sh and commit the script at the top level of your repository (the same directory your install_daemons.sh script should be located). 

# The preflight.sh script handles preconfiguration of your application. 
# The script will be called after the Postgres server is running and a new database has been created. 
# preflight.sh will be responsible for creating the tables needed by your LOST implementation 
# in that database and loading enough data for your LOST implementation's functionality to be tested. 

# If you are using mod_wsgi, preflight.sh should also copy the needed files into the $HOME/wsgi directory.


bash ./preflight.sh lost