The objective of this project is to create a miniblog web app. 

The app allows one user to login, logout, post status. 

This app is packaged by setuptools to allow for the installation in the local client's machine. 

Before use, choose virtualenv or root environment to install flask package:

        pip install -r /path/to/requirements.txt

  or    conda install flask

How to use it

1 edit the configuration (config) in the flaskr.py file or export an FLASKR_SETTINGS environment variable pointing to a configuration file.

2 install the app from the root (i.e. first miniblog folder) of the project directory
       bash: pbip install --editable .

3 Instruct flask to use the right application

       export FLASK_APP=miniblog
       export FLASK_DEBUG=true
4 initialize the database with this command:

       flask initdb
5 now you can run flaskr:

       flask run




      
   
