#!/usr/bin/python3
"""
HBNB Flask web application server
App listens on 0.0.0.0 port 5000
"""
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.teardown_appcontext
def close_storage(_):
    """
    Close storage
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    List all states
    """
    store = get_storage()
    states = store.all(State)
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
