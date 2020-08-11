import pandas as pd
import numpy as np
import requests

class Data_Generation:
    def __init__(self):
        self.tmdbUrl = "https://api.themoviedb.org/3/movie/"
        self.apiKey = "?api_key=ed6fc6c32b49d3aa62791649188d4579"

    def get_movie_details(self,movie_id):
        """
        Accepts only tmdb movie id which should be an integer
        performs TMDB API call and fetches the data related to the tmdb movie id
        :param movie_id:
        :return: response in json fromat
        """
        url = self.tmdbUrl+str(movie_id)+self.apiKey
        response = requests.get(url).json()
        return response

    def get_movie_reviews(self,movie_id):
        """
        Accepts only tmdb movie id which should be an integer
        performs TMDB API call and fetches the review data for the movie id
        :param movie_id:
        :return: response in json format
        """
        url=self.tmdbUrl+str(movie_id)+"/reviews"+self.apiKey
        response=requests.get(url).json()
        total_review = []
        for x in range(response['total_results']):
            total_review.append(response['results'][x]['content'])
        return ",".join(total_review)

    def get_movie_ratings(self,movie_id):
        """
        Accepts only tmdb movie id which should be an integer
        performs TMDB API call and fetches the ratings for a given movie id
        :return:
        """
        url = self.tmdbUrl+str(movie_id)+"/account_states"+self.apiKey
        response = requests.get(url).json()
        return response

    def get_cast_crew_details(self,movie_id):
        """
        Accetps only tmdb movie id which should be an integer
        Performs TMDB API Call and fetches the crew and cast details for a given movie id
        :param movie_id:
        :return:
        """
        url = self.tmdbUrl+str(movie_id)+"/credits"+self.apiKey
        response = requests.get(url).json()
        cast=[]
        for x in range(len(response['cast'])):
            cast.append(str(response['cast'][x]['name']).replace(" ","_"))
        crew = []
        for x in range(len(response['crew'])):
            if response['crew'][x]['job'] == "Director":
                crew.append(str(response['crew'][x]['name']).replace(" ","_"))
        return ",".join(crew+cast)

    def get_movie_keywords(self,movie_id):
        url=self.tmdbUrl+str(movie_id)+"/keywords"+self.apiKey
        response = requests.get(url).json()
        keywords = []
        for x in range(len(response['keywords'])):
            keywords.append(str(response['keywords'][x]['name']).replace(" ","_"))
        return ",".join(keywords)

    def prepare_data(self):
        """
        Accepts only integer value to control the number of api calls and number of records
        :param limit:
        :return:
        """
        movies = pd.read_csv("data/ml-latest/movies.csv")
        links = pd.read_csv("data/ml-latest/links.csv")
        data = pd.merge(movies,links,on="movieId",how="inner")
        data['info'] = data['tmdbId'].apply(lambda x: self.get_movie_details(x))
        data['overview'] = data['info'].apply(lambda x: x['overview'])
        data['popularity'] = data['info'].apply(lambda x: x['popularity'])
        data['overview'] = data['info'].apply(lambda x: x['overview'])
        data['original_title'] = data['info'].apply(lambda x: x['original_title'])
        data['vote_average'] = data['info'].apply(lambda x: x['vote_average'])
        data['vote_count'] = data['info'].apply(lambda x: x['vote_count'])
        data['tagline'] = data['info'].apply(lambda x: x['tagline'])
        data['budget'] = data['info'].apply(lambda x: x['budget'])
        data['reviews'] = data['tmdbId'].apply(lambda x: self.get_movie_reviews(x))
        data['Crew_Cast'] = data['tmdbId'].apply(lambda x: self.get_cast_crew_details(x))
        data['keywords'] = data['tmdbId'].apply(lambda x: self.get_movie_keywords(x))
        del data['imdbId']
        del data['info']
        try:
            data.to_csv("data/movie_data.csv")
            return "Data Generated Successfully"
        except:
            return "Failed to Generate Data"


