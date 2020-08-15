class StarWarsService:
    def __init__(self, repository):
        self._repository = repository

    def get_films(self):
        films = self._repository.get_films()
        output = []
        for film in films:
            film_obj = {
                'id': film[0],
                'title': film[1],
                'release_date': film[2]
            }
            output.append(film_obj)
        return output

    def get_characters(self, film_id: int):
        characters = self._repository.get_characters(film_id)
        output = []
        for character in characters:
            output.append({
                'id': character[0],
                'name': character[1]
            })
        return output
