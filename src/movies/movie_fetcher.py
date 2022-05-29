import requests
import re
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup

from movies.models import get_postgres_uri

DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        get_postgres_uri(),
        isolation_level="REPEATABLE READ",
    )
)
session = DEFAULT_SESSION_FACTORY()

class WebScrapper:
    def __init__(self, url = 'http://www.imdb.com/chart/top'):
        self.url = url
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        self.list_movies = []

    def scrape_data(self):
        movies = self.soup.select('td.titleColumn')
        links = [a.attrs.get('href') for a in self.soup.select('td.titleColumn a')]
        crew = [a.attrs.get('title') for a in self.soup.select('td.titleColumn a')]
        ratings = [b.attrs.get('data-value') for b in self.soup.select('td.posterColumn span[name=ir]')]
        votes = [b.attrs.get('data-value') for b in self.soup.select('td.ratingColumn strong')]

        return [movies, links, crew, ratings, votes]

    def movie_details(self):
        movies, links, crew, ratings, votes = self.scrape_data()

        for index in range(0, len(movies)):
            # Separating movie into: 'place',
            # 'title', 'year'
            movie_string = movies[index].get_text()
            movie = (' '.join(movie_string.split()).replace('.', ''))
            movie_title = movie[len(str(index)) + 1:-7]
            year = re.search('\((.*?)\)', movie_string).group(1)
            place = movie[:len(str(index)) - (len(movie))]

            data = {"movie_title": movie_title,
                    "year": year,
                    "place": place,
                    "star_cast": crew[index],
                    "rating": ratings[index],
                    "vote": votes[index],
                    "link": links[index],
                    "preference_key": index % 4 + 1}
            self.list_movies.append(data)
    
    def to_csv(self):
        fields = ["preference_key", "movie_title", "star_cast", "rating", "year", "place", "vote", "link"]
    
        with open("movie_results.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for movie in self.list_movies:
                writer.writerow({**movie})


