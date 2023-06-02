import json
import pandas as pd

from os import path


def read_json(path: str) -> dict:
    with open(path, 'r') as file:
        return json.load(file)


def read_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path, index_col='outcome_type')


#---------------------------------#


PARAMS = read_json(path.join(path.dirname(
    __file__), '..', 'settings', 'params.json'))


class Ratings():

    def __init__(self, path: pd.DataFrame, team_name: str):

        self.team_name = team_name
        self.data = read_csv(path)
        self.offensive_rating = 0
        self.defensive_rating = 0
        self.hustle_rating = 0
        self.discipline_rating = 0

    def calculate_rating(self, rating_name: str, team_name: str):

        is_successful = PARAMS[rating_name]['params_bool']
        coefs = PARAMS[rating_name]['params_weight']
        params = PARAMS[rating_name]['params']

        ratings = []

        for param in range(len(params)):

            self.data.loc[(self.data['type'] == params[param]) & (self.data.index == 'Successful') & (
                self.data['team'] == team_name)].index.value_counts()

            if is_successful:
                ratings.append(self.data.loc[(self.data['type'] == params[param]) & (self.data.index == 'Successful') & (
                    self.data['team'] == team_name)].index.value_counts().max() * coefs[param])
            else:
                ratings.append(self.data.loc[(self.data['type'] == params[param]) & (
                    self.data['team'] == team_name)].index.value_counts().max() * coefs[param])

            max_value = self.data[self.data['type'] ==
                                  params[param]]['team'].value_counts().max()
            ratings[-1] = (ratings[-1] * 100) / max_value

        return sum(ratings) / len(ratings)

    def construtor(self):
        self.offensive_rating = self.calculate_rating(
            'offensive_rating', self.team_name)
        self.defensive_rating = self.calculate_rating(
            'defensive_rating', self.team_name)
        self.hustle_rating = self.calculate_rating(
            'hustle_rating', self.team_name)
        self.discipline_rating = self.calculate_rating(
            'discipline_rating', self.team_name)

        return {
            'offensive_rating': self.offensive_rating,
            'defensive_rating': self.defensive_rating,
            'hustle_rating': self.hustle_rating,
            'discipline_rating': self.discipline_rating,
            'total_rating': (self.offensive_rating + self.defensive_rating + self.hustle_rating + self.discipline_rating)/4
        }
