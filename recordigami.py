import os
import json
import argparse
import pandas as pd
from seasons_parser import get_championship_team
from datetime import datetime

WNBA = 'WNBA'
NBA = 'NBA'
DIRNAME = os.path.abspath(os.path.dirname(__file__))
TEAMS_DIRECTORY = os.path.join(DIRNAME, 'teams')
SEASON_DIRECTORY = os.path.join(DIRNAME, 'seasons')
OUTPUT_DIRECTORY = os.path.join(DIRNAME, 'output')


def str_to_int(value, default=int(0)):
    stripped_value = value.strip()
    try:
        return int(stripped_value)
    except ValueError:
        return default


def get_historical_games(league):
	print('Getting all season data...')
	if league == WNBA:
		start_year = 1997
		end_year = 2020
	else:
		start_year = 1947
		end_year = 2021

	champions = {}
	seasons = []
	for year in list(range(start_year, end_year + 1)):
		try:
			champion = get_championship_team(year, league)
			if champion not in champions:
				champions[champion] = [year]
			else:
				champions[champion].append(year)
		except:
			champions = champions
		season = pd.read_csv('{0}/games_{1}({2}).csv'.format(SEASON_DIRECTORY, league, year))
		season = season.dropna(how='all')
		seasons.append(season)

	print('Combining all season data into single games dataframe...')
	games = pd.concat(seasons, ignore_index=True).sort_values(by='date', ascending=True)
	return games, champions


def get_historical_teams(league):
	print('Getting team metadata...')
	teams_csv = pd.read_csv('{0}/{1}_teams.csv'.format(TEAMS_DIRECTORY, league.lower())).fillna(0)
	teams = {}
	for index, team in teams_csv.iterrows():
		name = team['team']
		parent = team['parent']
		history = team['history']

		# https://teamcolorcodes.com
		primary_color = team['primary_color']
		secondary_color = team['secondary_color']
		tertiary_color = team['tertiary_color']

		teams[name] = {
			'primary_color': primary_color,
			'secondary_color': secondary_color,
			'tertiary_color': tertiary_color,
			'parent': parent,
			'history': history
		}
	return teams


def get_historical_recordigami(games, teams, league):
	print('Creating recordigami JSON object...')
	recordigami = {}
	recordigami_check = {}
	for index, game in games.iterrows():
		team = game['id']
		wins = game['win']
		losses = game['loss']
		year = int(datetime.utcfromtimestamp(int(game['date'])).strftime('%Y'))

		win_string = str(int(wins)) if len(str(int(wins))) == 2 else '0' + str(int(wins))
		loss_string = str(int(losses)) if len(str(int(losses))) == 2 else '0' + str(int(losses))
		win_loss_key = win_string + loss_string
		is_recordigami = win_loss_key not in recordigami_check

		if year not in recordigami:
			recordigami[year] = {}

		if is_recordigami:
			recordigami_check[win_loss_key] = year
			recordigami[year][win_loss_key] = {
				# TODO: move this into the d3 logic accessing separate object
				"primary_color": teams[team]['primary_color'],
				"secondary_color": teams[team]['secondary_color'],
				"tertiary_color": teams[team]['tertiary_color'],
				"parent": teams[team]["parent"],

				"team": team,
				"win": wins,
				"loss": losses,
				"date": game['date'],
				"year": year,
				"end_of_season": (wins + losses) == 82,
				"count": 1
			}
		if not is_recordigami:
			relevant_year = recordigami_check[win_loss_key]
			recordigami[relevant_year][win_loss_key]['count'] += 1

	return recordigami


def get_historical_season_paths(champions, games, teams, league):
	print('Creating season paths JSON object...')
	season_win_loss = []
	season_paths = {}
	for team in teams.keys():
		championship_seasons = champions[team] if team in champions else []
		team_games = games[games['id'] == team]

		max_occurrences = 0
		seasons = {}
		cumulative_seasons = []
		win_loss_counter = {}
		for year in team_games.year.unique():
			season_games = team_games[team_games['year'] == year]
			season_path = {'0000': {'win': 0, 'loss': 0}}

			for index, game in season_games.iterrows():
				# team = game['id']
				wins = game['win']
				losses = game['loss']

				win_string = str(int(wins)) if len(str(int(wins))) == 2 else '0' + str(int(wins))
				loss_string = str(int(losses)) if len(str(int(losses))) == 2 else '0' + str(int(losses))
				win_loss_key = win_string + loss_string
				if win_loss_key not in win_loss_counter:
					win_loss_counter[win_loss_key] = 1
				else:
					win_loss_counter[win_loss_key] += 1
					# Update max_occurrences - useful for opacity
					num_occurrences = win_loss_counter[win_loss_key]
					if num_occurrences > max_occurrences:
						max_occurrences = num_occurrences

				season_path[win_loss_key] = {'win': wins, 'loss': losses}
				seasons[int(year)] = season_path

			season_win_loss.append({
				'year': int(year),
				'win': wins,
				'loss': losses,
				'win_pct': round(float(float(wins) / float(wins + losses)), 3),
				'team': team,
				'is_championship': year in championship_seasons
			})


		cumulative_seasons = calculate_cumulative_seasons(win_loss_counter)
		season_paths[team] = {
			'seasons': seasons,
			'cumulative_seasons': cumulative_seasons,
			'championship_seasons': championship_seasons,
			'max_count': max_occurrences
		}
	return season_paths, season_win_loss


def calculate_cumulative_seasons(win_loss_counter):
	cumulative_seasons = [{'win': 0, 'loss': 0, 'count': 1}]
	for key, value in win_loss_counter.items():
		wins = str_to_int(key[0:2])
		losses = str_to_int(key[2:])
		cumulative_seasons.append({
			'win': wins,
			'loss': losses,
			'count': value
		})
	return cumulative_seasons


def output_recordigami_files(league=WNBA):
	games, champions = get_historical_games(league)
	teams = get_historical_teams(league)
	recordigami = get_historical_recordigami(games, teams, league)
	season_paths, season_win_loss = get_historical_season_paths(champions, games, teams, league)


	games.to_csv('{0}/{1}_games.csv'.format(OUTPUT_DIRECTORY, league), index=False)
	with open('{0}/{1}_teams.json'.format(OUTPUT_DIRECTORY, league), 'w') as file: json.dump(teams, file)
	with open('{0}/{1}_recordigami.json'.format(OUTPUT_DIRECTORY, league), 'w') as file: json.dump(recordigami, file)
	with open('{0}/{1}_season_paths.json'.format(OUTPUT_DIRECTORY, league), 'w') as file: json.dump(season_paths, file)
	with open('{0}/{1}_season_win_loss.json'.format(OUTPUT_DIRECTORY, league), 'w') as file: json.dump(season_win_loss, file)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Get historical recordigami array')
	parser.add_argument('--league', type=str, help='WNBA or NBA')

	args = parser.parse_args()
	league = args.league
	output_recordigami_files(league)



