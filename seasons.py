import os
from titlecase import titlecase
from datetime import datetime
import pandas as pd
import argparse
from seasons_parser import get_season_schedule, get_correct_team_name

WNBA = 'WNBA'
NBA = 'NBA'

START_YEAR = END_YEAR = datetime.now().year

DIRNAME = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIRECTORY = os.path.join(DIRNAME, 'seasons')

def update_win_loss_dict(team_name, game_type, win_loss_dict={}):
	if team_name not in win_loss_dict:
		win_loss_dict[team_name] = {
			'win': 0,
			'loss': 0,
		}
	win_loss_dict[team_name][game_type] = win_loss_dict[team_name][game_type] + 1


def get_wnba_num_teams(season_year):
	# 1997 - 2009 the number of teams varied, then stabilized at 12 from 2010 - 2020
	num_teams_1997_2009 = [8,10,12,16,16,16,14,13,13,14,13,14,13]
	if season_year <= 2009:
		index = season_year - 1997
		num_teams = num_teams_1997_2009[index]
	else:
		num_teams = 12
	return num_teams


def get_wnba_num_games(season_year):
	# Number of games has varied, stabilized for many years at 34, and is at 36 in 2020
	if season_year == 1997:
		num_games = 28
	elif season_year == 1998:
		num_games = 30
	elif season_year <= 2002:
		num_games = 32
	elif season_year <= 2019:
		num_games = 34
	elif season_year == 2020:
		num_games = 22
	else:
		num_games = 36
	return num_games


def get_nba_num_teams(season_year):
	num_teams_1947_1955 = [11,8,12,17,11,10,10,9,9]
	if season_year <= 1955:
		index = season_year - 1947
		num_teams = num_teams_1947_1955[index]
	elif season_year <= 1961:
		num_teams = 8
	elif season_year <= 1966: 
		num_teams = 9
	elif season_year == 1967:
		num_teams = 10
	elif season_year == 1968:
		num_teams = 12
	elif season_year <= 1970:
		num_teams = 14
	elif season_year <= 1971:
		num_teams = 17
	elif season_year <= 1976:
		num_teams = 18
	elif season_year <= 1980:
		num_teams = 22
	elif season_year <= 1988:
		num_teams = 23
	elif season_year == 1989:
		num_teams = 25
	elif season_year <= 1995:
		num_teams = 27
	elif season_year <= 2004:
		num_teams = 29
	else:
		num_teams = 30
	return num_teams


def get_nba_num_games(season_year, team=None):
	# Number of games varied over the first 20 years, stabilized at 82 except for lockouts/covid
	if season_year == 1947:
		if team not in ['St. Louis Bombers', 'Chicago Stags']:
			num_games = 60
		else:
			num_games = 61
	elif season_year == 1948:
		num_games = 48
	elif season_year == 1949:
		num_games = 60
	elif season_year == 1950:
		if team in ['Anderson Packers', 'Indianapolis Olympians', 'Syracuse Nationals', 'Tri-Cities Blackhawks']:
			num_games = 64
		elif team in ['Sheboygan Red Skins', 'Waterloo Hawks', 'Denver Nuggets']:
			num_games = 62
		else:
			num_games = 68
	elif season_year == 1951:
		if team in ['Boston Celtics']:
			num_games = 69
		elif team in ['Syracuse Nationals', 'New York Knicks', 'Philadelphia Warriors', 'Baltimore Bullets']:
			num_games = 66
		elif team in ['Washington Capitols']:
			num_games = 35
		else:
			num_games = 68
	elif season_year == 1952:
		num_games = 66
	elif season_year == 1953:
		if team in ['Rochester Royals', 'New York Knicks', 'Minneapolis Lakers', 'Baltimore Bullets']:
			num_games = 70
		elif team in ['Fort Wayne Pistons', 'Philadelphia Warriors']:
			num_games = 69
		else:
			num_games = 71
	elif season_year <= 1959:
		num_games = 72
	elif season_year == 1960:
		num_games = 75
	elif season_year == 1961:
		num_games = 79
	elif season_year <= 1966:
		num_games = 80
	elif season_year == 1967:
		num_games = 81
	elif season_year == 1999:
		num_games = 50
	elif season_year == 2012:
		num_games = 66
	elif season_year == 2020:
		if team in ['Portland Trail Blazers']:
			num_games = 74
		elif team in ['Milwaukee Bucks', 'Indiana Pacers', 'Miami Heat', 'Philadelphia 76ers', 'Orlando Magic', 'Denver Nuggets', 'Memphis Grizzlies', 'Phoenix Suns']:
			num_games = 73
		elif team in ['Toronto Raptors', 'Boston Celtics', 'Brooklyn Nets', 'Washington Wizards', 'Los Angeles Clippers', 'Houston Rockets', 'Oklahoma City Thunder', 'Utah Jazz', 'Sacramento Kings', 'New Orleans Pelicans']:
			num_games = 72
		elif team in ['Los Angeles Lakers', 'San Antonio Spurs']:
			num_games = 71
		elif team in ['Atlanta Hawks']:
			num_games = 67
		elif team in ['New York Knicks', 'Detroit Pistons']:
			num_games = 66
		elif team in ['Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Golden State Warriors']:
			num_games = 65
		elif team in ['Minnesota Timberwolves']:
			num_games = 64
		else:
			num_games = 75
	elif season_year == 2021:
		num_games = 72
	else:
		num_games = 82
	return num_games


def output_season_paths(season_year=END_YEAR, league=WNBA):
	# season_year is the end year of a season (e.g. for 2010-11, season_year=2011)
	print('Retrieving {0} season paths for {1}...'.format(league, season_year))
	i = 0 
	if league == WNBA:
		num_teams = get_wnba_num_teams(season_year)
		num_games = get_wnba_num_games(season_year)

	if league == NBA:
		num_teams = get_nba_num_teams(season_year)
		num_games = get_nba_num_games(season_year)

	num_regular_season_games = num_teams*num_games
	nba_columns = ['id', 'home_team', 'away_team', 'win', 'loss', 'game_number', 'date', 'year']
	nba_df = pd.DataFrame(index=range(num_regular_season_games), columns=nba_columns)
	win_loss_dict = {}

	# for game in client.season_schedule(season_year=season_year):
	for game in get_season_schedule(season_year=season_year, league=league):
		date = game['start_time'].timestamp()
		home_team = get_correct_team_name(titlecase(game['home_team'].value), season_year, league)
		away_team = get_correct_team_name(titlecase(game['away_team'].value), season_year, league)

		if game['home_team_score'] is None:
			continue

		winning_team_name = home_team if game['home_team_score'] > game['away_team_score'] else away_team
		losing_team_name = home_team if winning_team_name == away_team else away_team
		update_win_loss_dict(winning_team_name, 'win', win_loss_dict)
		update_win_loss_dict(losing_team_name, 'loss', win_loss_dict)

		home_wins = win_loss_dict[home_team]['win']
		home_losses = win_loss_dict[home_team]['loss']
		home_game_number = home_wins + home_losses

		away_wins = win_loss_dict[away_team]['win']
		away_losses = win_loss_dict[away_team]['loss']
		away_game_number = away_wins + away_losses


		if league == NBA and season_year in [1947, 1950, 1951, 1953, 2020] and num_games > 35:
			if home_game_number > get_nba_num_games(season_year, home_team):
				continue
			if away_game_number > get_nba_num_games(season_year, away_team):
				continue
				
		if home_game_number > num_games or away_game_number > num_games:
			continue

		nba_df.iloc[i,] = [home_team, home_team, away_team, home_wins, home_losses, home_game_number, date, season_year]
		nba_df.iloc[i+1,] = [away_team, home_team, away_team, away_wins, away_losses, away_game_number, date, season_year]
		i = i + 2
		if i == num_regular_season_games:
			break

	nba_df.sort_values(by=['id', 'game_number']).to_csv('{0}/games_{1}({2}).csv'.format(OUTPUT_DIRECTORY, league, season_year), index=False)
	print('Finished {0}'.format(season_year))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Download NBA season schedule data')
	parser.add_argument('--start', type=int, help='Year of the end of an NBA season')
	parser.add_argument('--end', type=int, help='Year of the end of an NBA season')
	parser.add_argument('--league', type=str, help='WNBA or NBA')

	args = parser.parse_args()
	league = args.league

	if league == WNBA:
		START_YEAR = 1997
		END_YEAR = 2020
	else:
		START_YEAR = 1947
		END_YEAR = 2021

	start = args.start or START_YEAR
	end = args.end or END_YEAR
	
	for year in list(range(start, end + 1)):
		output_season_paths(year, league)

