import sys
from src.utils.json_func import read_json
import os
from src.utils.ratings import Ratings

def main(league,team_name):
    countries = read_json(os.path.join(os.path.dirname(__file__), 'src','settings', 'countries.json'))
    team_res= Ratings(countries[league],team_name)
    return team_res.construtor()

if __name__ == '__main__':
    print(main(sys.argv[1],sys.argv[2]))