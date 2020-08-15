from flask import Blueprint, jsonify


class StarWarsController:
    def __init__(self, service):
        self._service = service
        self._blueprint = Blueprint('startwars', __name__)
        self._blueprint.add_url_rule('/films',
                                     None,
                                     self.get_films,
                                     methods=['GET'])
        self._blueprint.add_url_rule('/films/<int:film_id>/characters',
                                     None,
                                     self.get_characters,
                                     methods=['GET'])

    def get_bluprint(self):
        return self._blueprint

    def get_films(self):
        films = self._service.get_films()
        return jsonify(films)

    def get_characters(self, film_id):
        characters = self._service.get_characters(film_id)
        return jsonify(characters)
