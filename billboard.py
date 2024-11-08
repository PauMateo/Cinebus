import requests
import json
from dataclasses import dataclass
from bs4 import BeautifulSoup as BSoup
from typing import TypeAlias
from constants import cinemas_coords


Coord:  TypeAlias = tuple[float, float]   # (latitude, longitude)


@dataclass
class Film:
    title: str
    genres: list[str]
    director: str
    actors: list[str]


@dataclass
class Cinema:
    name: str
    address: str
    coord: Coord


@dataclass
class Projection:
    film: Film
    cinema: Cinema
    start: tuple[int, int]  # start time
    end: tuple[int, int]  # end time
    duration: int  # minutes
    language: str  # V.O or Spanish


@dataclass
class Billboard:
    films: list[Film]
    cinemas: list[Cinema]
    projections: list[Projection]
    poss_filters: list[str]  # llista de possibles filtres que es poden aplicar
    genres: set[str]  # conjunt dels diferents gèneres de les películes

    def __init__(self, f: list[Film] = [], c: list[Cinema] = [],
                 p: list[Projection] = [], g: set[str] = set()):
        '''Constructor'''

        self.films = f
        self.cinemas = c
        self.projections = p
        self.poss_filters = ['genre', 'director', 'film', 'cinema',
                             'time', 'duration', 'language', 'city']
        self.genres = g

    def filter(self, filters: dict[str, str]) -> list[Projection]:
        '''Returns the billboard applying the given filter. The possible types
         of filters are in the self.poss_filters list. The format is:
         {filter_type: filter}.
         - The time filter returns projections that
         they start and end within the time indicated, and the format is:
         {time: hh:mm-hh:mm} (start-end).
         - The duration filter returns all duration projections
         equal to or less than given, in minutes.
         The genre filter returns all projections that are of
         given genres, and the format is: {genre: genre1-genre2-...}. they can
         give multiple genders. All other filters work as expected.
        '''

        try:
            assert all([k in self.poss_filters for k in filters.keys()])

            return [x for x in self.projections if
                    all([self._apply_filter(x, f) for f in filters.items()])]

        except Exception:
            raise ValueError

    def _filter_time(self, x: Projection, filter: str) -> bool:
        '''Apply the schedule filter to the projection x.
        Returns True if the schedule of the
        given projection is included within the filter.
        '''
        s, e = filter.split('-')
        start = tuple(map(int, s.split(':')))
        end: tuple[int, int] = tuple(map(int, e.split(':')))

        # we need to check separated cases, because a film can
        # start and end on diferent days:
        if end < start:
            return (start <= x.start) and \
                        (start <= x.end <= (end[0]+24, end[1]))
        elif x.end < x.start:
            return (start <= x.start) and \
                        (start <= (x.end[0]+24, x.end[1]) <= end)
        return (start <= x.start) and (start <= x.end <= end)

    def _filter_duration(self, x: Projection, filter: str) -> bool:
        '''Duration filter. Returns true if the projection x
        has a duration equal to or less than the given one'''
        return x.duration <= int(filter)

    def _filter_cinema(self, x: Projection, filter: str) -> bool:
        '''Cinema Filter. Returns True if the name of the cinema of the
        projection it's equal to the given one.'''
        return x.cinema.name == filter

    def _filter_genre(self, x: Projection, filter: str) -> bool:
        '''Genre Filter. Returns True if the genre of the film of the
        projection x is included within the given genre.'''
        return all([g in x.film.genres for g in filter.split('-')])

    def _filter_film(self, x: Projection, filter: str) -> bool:
        '''Film Filter. Returns True if the name of the film of the
        projection x it's equal to the given one.'''
        return x.film.title == filter

    def _filter_language(self, x: Projection, filter: str) -> bool:
        '''Language Filter. Returns True if the language of the
        projection is the given one.'''
        return x.language == filter

    def _filter_director(self, x: Projection, filter: str) -> bool:
        '''Director Filter. Returns True if the director of the film of the
        projection x it's the given one.'''
        return x.language == filter

    def _filter_city(self, x: Projection, filter: str) -> bool:
        '''City Filter. Returns True if the cinema of the projection x
        is in the given city.'''
        return filter in x.cinema.address

    def _apply_filter(self, x: Projection, flt: tuple[str, str]) -> bool:
        '''Applies de filter given to the projection x by redirecting
        it to the specific filter functions.'''

        return getattr(self, '_filter_' + flt[0])(x, flt[1])


def read() -> Billboard:
    '''Function that downloads the necessary data
    and returns the current day's billboard.
    '''
    bboard: Billboard = Billboard()

    urls = [
        "https://www.sensacine.com/cines/cines-en-72480/",
        "https://www.sensacine.com/cines/cines-en-72480/?page=2",
        "https://www.sensacine.com/cines/cines-en-72480/?page=3"]

    for url in urls:
        try:
            r = requests.get(url)
        except Exception:
            print(f'Error substracting billboard from {url}')
            return bboard  # retorna cartellera buida
        try:
            soup = BSoup(r.content, "lxml")
        except Exception:
            print('Error at module BeatifulSoup; check that module ' +
                  "'lxml' is installed.")
            return bboard

        # comencem el web scraping
        headers = soup.find_all('div', class_="margin_10b j_entity_container")
        panels = soup.find_all('div', class_='tabs_box_panels')

        cinema: Cinema
        film: Film
        projection: Projection

        for i in range(len(headers)):
            # construir cinema:
            name = headers[i].a.text[1:-1]
            address = headers[i].find_all(
                'span', class_="lighten")[1].text[1:-1]

            cinema = Cinema(name, address, cinemas_coords[name])
            bboard.cinemas.append(cinema)

            # today's panel is:
            actual_panel = panels[i].find('div', class_='item-0')

            if actual_panel is None:
                continue
            # build films; iterate through the current cinema's films
            for info in actual_panel.find_all('div', class_='item_resa'):

                data = json.loads(info.find('div', class_='j_w')['data-movie'])
                film = Film(data['title'],
                            data['genre'],
                            data['directors'][0],
                            data['actors'])

                for genre in data['genre']:
                    bboard.genres.add(genre)
                if film not in bboard.films:
                    bboard.films.append(film)

                # build projections
                if info.span.text == 'Digital':
                    language = 'V.O.'
                else:
                    language = 'Spanish'

                for session in info.find_all('em'):
                    start: tuple[int, int]
                    end: tuple[int, int]
                    duration: int

                    times = json.loads(session['data-times'])

                    start = times[0].split(':')
                    start = int(start[0]), int(start[1])
                    end = times[2].split(':')
                    end = int(end[0]), int(end[1])
                    if end < start:
                        duration = (end[0] + 24 - start[0]) * \
                            60 + end[1] - start[1]
                    else:
                        duration = (end[0] - start[0]) * 60 + end[1] - start[1]

                    projection = Projection(film, cinema,
                                            start, end, duration, language)
                    bboard.projections.append(projection)

    bboard.projections.sort(key=lambda t: t.start)
    bboard.cinemas.sort(key=lambda c: c.name)
    bboard.films.sort(key=lambda f: f.title)

    return bboard
