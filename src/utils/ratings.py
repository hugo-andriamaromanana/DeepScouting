from json_func import * 
from pandas_func import *

PARAMS = read_json(path.join(path.dirname(
    __file__), 'settings', 'params.json'))

class Ratings():

    def __init__(self, path: pd.DataFrame, team_name: str):

        self.team_name = team_name
        self.data = read_csv(path)
        self.offensive_rating = 0
        self.defensive_rating = 0
        self.strategy_rating = 0
        self.hustle_rating = 0
        self.discipline_rating = 0

    def calculate_rating(self, rating_name: str, team_name: str):

        is_successful = PARAMS[rating_name]['params_bool']
        coefs = PARAMS[rating_name]['params_weight']
        params = PARAMS[rating_name]['params']

        ratings = []

        for param in range(len(params)):

            if is_successful[param]:
                ratings.append(self.data.loc[(self.data['type'] == params[param]) & (
                    self.data.index == 'Successful') & (self.data['team'] == team_name)].index.value_counts())
            else:
                ratings.append(self.data.loc[(self.data['type'] == params[param]) & (
                    self.data.index == 'Unsuccessful') & (self.data['team'] == team_name)].index.value_counts())

        return sum([ratings[i] * coefs[i] for i in range(len(ratings))])

    def construtor(self):
        self.offensive_rating = self.calculate_rating(
            'offensive_rating', self.team_name)
        self.defensive_rating = self.calculate_rating(
            'defensive_rating', self.team_name)
        self.strategy_rating = self.calculate_rating(
            'strategy_rating', self.team_name)
        self.hustle_rating = self.calculate_rating(
            'hustle_rating', self.team_name)
        self.discipline_rating = self.calculate_rating(
            'discipline_rating', self.team_name)
        
        if self.offensive_rating.isnull().any():
            self.offensive_rating = pd.Series([0])
        if self.defensive_rating.isnull().any():
            self.defensive_rating = pd.Series([0])
        if self.strategy_rating.isnull().any():
            self.strategy_rating = pd.Series([0])
        if self.hustle_rating.isnull().any():
            self.hustle_rating = pd.Series([0])
        if self.discipline_rating.isnull().any():
            self.discipline_rating = pd.Series([0])
        
        return {
            'offensive_rating': self.offensive_rating.iloc[0],
            'defensive_rating': self.defensive_rating.iloc[0],
            'strategy_rating': self.strategy_rating.iloc[0],
            'hustle_rating': self.hustle_rating.iloc[0],
            'discipline_rating': self.discipline_rating.iloc[0],
            'total_rating': (self.offensive_rating.iloc[0] + self.defensive_rating.iloc[0] + self.strategy_rating.iloc[0] + self.hustle_rating.iloc[0] + self.discipline_rating.iloc[0])/5
        }