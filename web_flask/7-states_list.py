#!/usr/bin/python3
"""
HBNB Flask web application server
App listens on 0.0.0.0 port 5000
"""
from flask import Flask, render_template, g
from models import storage
from models.state import State
app = Flask(__name__)

def get_storage():
    """
    Get storage instance
    """
    if not hasattr(g, 'storage'):
        g.storage = storage
    return g.storage

@app.teardown_appcontext
def close_storage(exception):
    """
    Close storage
    """
    store = g.pop('storage', None)
    if store is not None:
        store.close()

@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    List all states
    """
    store = get_storage()
    states = store.all(State)
    return render_template('7-states_list.html', states=states)


# @app.route('/', strict_slashes=False)
# def hello_hbnb():
#     """
#     Hello HBNB!
#     """
#     return 'Hello HBNB!'
# @app.route('/hbnb', strict_slashes=False)
# def hbnb():
#     """
#     HBNB
#     """
#     return 'HBNB'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
