#  UFind API

### Generating a Virtual Environment

We'll be using `virtualenv` to generate a virtual environment for our development environment to better manage our python3 modules. Run the following command to generate one after you've installed `virtualenv`

[To install virtualenv, click here](https://virtualenv.pypa.io/en/stable/installation/)

`virtualenv -p python3 venv`

### Development

To activate the virtual env. run:

`source path/to/venv/bin/activate`

Before the server can be started, remember to install all of the python3 modules with 

`pip3 install -r requirements.txt`

Once that's done, start the API by running:

`python3 run.py`

The API will be available at localhost, or 127.0.0.1, at port 8080. This can be changed in /config.py

To deactiave run:

`deactivate`

### Docs Link

Remeber the API is changing, so the docs may not be as accurate. Your best friend will be the code or Daniel :D

[API Docs](https://danielsantos.docs.apiary.io)
