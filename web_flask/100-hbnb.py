#!/usr/bin/python3
"""
HBNB Flask web application server
App listens on 0.0.0.0 port 5000
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.user import User

app = Flask(__name__)


@app.teardown_appcontext
def close_storage(_=None):
    """
    Close storage
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    List all states
    """
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """
    List all cities by states
    """
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """
    List all states or state by id
    """
    states = storage.all(State)
    state = None
    if id:
        key = f"State.{id}"
        if key in states:
            state = states[key]
        else:
            states = None
    return render_template('9-states.html', states=states, state=state)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """
    List all states and amenities
    """
    states = storage.all(State)
    amenities = storage.all(Amenity)
    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    List all states and amenities
    """
    states = storage.all(State)
    amenities = storage.all(Amenity)
    places = storage.all(Place)
    return render_template('100-hbnb.html', states=states,
                           amenities=amenities, places=places)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
