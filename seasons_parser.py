import requests
import re
import csv
from lxml import html
from datetime import datetime
from enum import Enum
import pytz

BAA = 'BAA'
NBA = 'NBA'
WNBA = 'WNBA'

class Team(Enum):
    # WNBA
    ATLANTA_DREAM = "ATLANTA DREAM"
    CHICAGO_SKY = "CHICAGO SKY"
    CONNECTICUT_SUN = "CONNECTICUT SUN"
    DALLAS_WINGS = "DALLAS WINGS"
    INDIANA_FEVER = "INDIANA FEVER"
    LAS_VEGAS_ACES = "LAS VEGAS ACES"
    LOS_ANGELES_SPARKS = "LOS ANGELES SPARKS"
    MINNESOTA_LYNX = "MINNESOTA LYNX"
    NEW_YORK_LIBERTY = "NEW YORK LIBERTY"
    PHOENIX_MERCURY = "PHOENIX MERCURY"
    SEATTLE_STORM = "SEATTLE STORM"
    WASHINGTON_MYSTICS = "WASHINGTON MYSTICS"

    # WNBA DEPRECATED TEAMS
    CHARLOTTE_STING = "CHARLOTTE STING"
    CLEVELAND_ROCKERS = "CLEVELAND ROCKERS"
    DETROIT_SHOCK = "DETROIT SHOCK"
    HOUSTON_COMETS = "HOUSTON COMETS"
    MIAMI_SOL = "MIAMI SOL"
    ORLANDO_MIRACLE = "ORLANDO MIRACLE"
    PORTLAND_FIRE = "PORTLAND FIRE"
    SACRAMENTO_MONARCHS = "SACRAMENTO MONARCHS"
    SAN_ANTONIO_SILVER_STARS = "SAN ANTONIO SILVER STARS"
    TULSA_SHOCK = "TULSA SHOCK"
    UTAH_STARZZ = "UTAH STARZZ"

    # NBA
    ATLANTA_HAWKS = "ATLANTA HAWKS"
    BOSTON_CELTICS = "BOSTON CELTICS"
    BROOKLYN_NETS = "BROOKLYN NETS"
    CHARLOTTE_HORNETS = "CHARLOTTE HORNETS"
    CHICAGO_BULLS = "CHICAGO BULLS"
    CLEVELAND_CAVALIERS = "CLEVELAND CAVALIERS"
    DALLAS_MAVERICKS = "DALLAS MAVERICKS"
    DENVER_NUGGETS = "DENVER NUGGETS"
    DETROIT_PISTONS = "DETROIT PISTONS"
    GOLDEN_STATE_WARRIORS = "GOLDEN STATE WARRIORS"
    HOUSTON_ROCKETS = "HOUSTON ROCKETS"
    INDIANA_PACERS = "INDIANA PACERS"
    LOS_ANGELES_CLIPPERS = "LOS ANGELES CLIPPERS"
    LOS_ANGELES_LAKERS = "LOS ANGELES LAKERS"
    MEMPHIS_GRIZZLIES = "MEMPHIS GRIZZLIES"
    MIAMI_HEAT = "MIAMI HEAT"
    MILWAUKEE_BUCKS = "MILWAUKEE BUCKS"
    MINNESOTA_TIMBERWOLVES = "MINNESOTA TIMBERWOLVES"
    NEW_ORLEANS_PELICANS = "NEW ORLEANS PELICANS"
    NEW_YORK_KNICKS = "NEW YORK KNICKS"
    OKLAHOMA_CITY_THUNDER = "OKLAHOMA CITY THUNDER"
    ORLANDO_MAGIC = "ORLANDO MAGIC"
    PHILADELPHIA_76ERS = "PHILADELPHIA 76ERS"
    PHOENIX_SUNS = "PHOENIX SUNS"
    PORTLAND_TRAIL_BLAZERS = "PORTLAND TRAIL BLAZERS"
    SACRAMENTO_KINGS = "SACRAMENTO KINGS"
    SAN_ANTONIO_SPURS = "SAN ANTONIO SPURS"
    TORONTO_RAPTORS = "TORONTO RAPTORS"
    UTAH_JAZZ = "UTAH JAZZ"
    WASHINGTON_WIZARDS = "WASHINGTON WIZARDS"

    # NBA DEPRECATED TEAMS
    ANDERSON_PACKERS = "ANDERSON PACKERS"
    BALTIMORE_BULLETS = "BALTIMORE BULLETS"
    BUFFALO_BRAVES = "BUFFALO BRAVES"
    CAPITAL_BULLETS = "CAPITAL BULLETS"
    CHARLOTTE_BOBCATS = "CHARLOTTE BOBCATS"
    CHICAGO_PACKERS = "CHICAGO PACKERS"
    CHICAGO_STAGS = "CHICAGO STAGS"
    CHICAGO_ZEPHYRS = "CHICAGO ZEPHYRS"
    CINCINNATI_ROYALS = "CINCINNATI ROYALS"
    CLEVELAND_REBELS = "CLEVELAND REBELS"
    DETROIT_FALCONS = "DETROIT FALCONS"
    FORT_WAYNE_PISTONS = "FORT WAYNE PISTONS"
    INDIANAPOLIS_JETS = "INDIANAPOLIS JETS"
    INDIANAPOLIS_OLYMPIANS = "INDIANAPOLIS OLYMPIANS"
    KANSAS_CITY_KINGS = "KANSAS CITY KINGS"
    KANSAS_CITY_OMAHA_KINGS = "KANSAS CITY-OMAHA KINGS"
    MINNEAPOLIS_LAKERS = "MINNEAPOLIS LAKERS"
    MILWAUKEE_HAWKS = "MILWAUKEE HAWKS"
    NEW_JERSEY_NETS = "NEW JERSEY NETS"
    NEW_ORLEANS_HORNETS = "NEW ORLEANS HORNETS"
    NEW_ORLEANS_JAZZ = "NEW ORLEANS JAZZ"
    NEW_ORLEANS_OKLAHOMA_CITY_HORNETS = "NEW ORLEANS/OKLAHOMA CITY HORNETS"
    NEW_YORK_NETS = "NEW YORK NETS"
    PITTSBURGH_IRONMEN = "PITTSBURGH IRONMEN"
    PHILADELPHIA_WARRIORS = "PHILADELPHIA WARRIORS"
    PROVIDENCE_STEAMROLLERS = "PROVIDENCE STEAMROLLERS"
    ROCHESTER_ROYALS = "ROCHESTER ROYALS"
    SAN_DIEGO_CLIPPERS = "SAN DIEGO CLIPPERS"
    SAN_DIEGO_ROCKETS = "SAN DIEGO ROCKETS"
    SAN_FRANCISCO_WARRIORS = "SAN FRANCISCO WARRIORS"
    SEATTLE_SUPERSONICS = "SEATTLE SUPERSONICS"
    SHEBOYGAN_RED_SKINS = "SHEBOYGAN RED SKINS"
    ST_LOUIS_BOMBERS = "ST. LOUIS BOMBERS"
    ST_LOUIS_HAWKS = "ST. LOUIS HAWKS"
    SYRACUSE_NATIONALS = "SYRACUSE NATIONALS"
    TORONTO_HUSKIES = "TORONTO HUSKIES"
    TRI_CITIES_BLACKHAWKS = "TRI-CITIES BLACKHAWKS"
    VANCOUVER_GRIZZLIES = "VANCOUVER GRIZZLIES"
    WASHINGTON_BULLETS = "WASHINGTON BULLETS"
    WASHINGTON_CAPITOLS = "WASHINGTON CAPITOLS"
    WATERLOO_HAWKS = "WATERLOO HAWKS"


TEAM_NAME_TO_TEAM = {
    # WNBA TEAMS
    "ATLANTA DREAM": Team.ATLANTA_DREAM,
    "CHICAGO SKY": Team.CHICAGO_SKY,
    "CONNECTICUT SUN": Team.CONNECTICUT_SUN,
    "DALLAS WINGS": Team.DALLAS_WINGS,
    "INDIANA FEVER": Team.INDIANA_FEVER,
    "LAS VEGAS ACES": Team.LAS_VEGAS_ACES,
    "LOS ANGELES SPARKS": Team.LOS_ANGELES_SPARKS,
    "MINNESOTA LYNX": Team.MINNESOTA_LYNX,
    "NEW YORK LIBERTY": Team.NEW_YORK_LIBERTY,
    "PHOENIX MERCURY": Team.PHOENIX_MERCURY,
    "SEATTLE STORM": Team.SEATTLE_STORM,
    "WASHINGTON MYSTICS": Team.WASHINGTON_MYSTICS,
    
    # WNBA DEPRECATED TEAMS
    "CHARLOTTE STING": Team.CHARLOTTE_STING,
    "CLEVELAND ROCKERS": Team.CLEVELAND_ROCKERS,
    "DETROIT SHOCK": Team.DETROIT_SHOCK,
    "HOUSTON COMETS": Team.HOUSTON_COMETS,
    "MIAMI SOL": Team.MIAMI_SOL,
    "ORLANDO MIRACLE": Team.ORLANDO_MIRACLE,
    "PORTLAND FIRE": Team.PORTLAND_FIRE,
    "SACRAMENTO MONARCHS": Team.SACRAMENTO_MONARCHS,
    "SAN ANTONIO SILVER STARS": Team.SAN_ANTONIO_SILVER_STARS,
    "TULSA SHOCK": Team.TULSA_SHOCK,
    "UTAH STARZZ": Team.UTAH_STARZZ,

    # NBA TEAMS
    "ATLANTA HAWKS": Team.ATLANTA_HAWKS,
    "BOSTON CELTICS": Team.BOSTON_CELTICS,
    "BROOKLYN NETS": Team.BROOKLYN_NETS,
    "CHARLOTTE HORNETS": Team.CHARLOTTE_HORNETS,
    "CHICAGO BULLS": Team.CHICAGO_BULLS,
    "CLEVELAND CAVALIERS": Team.CLEVELAND_CAVALIERS,
    "DALLAS MAVERICKS": Team.DALLAS_MAVERICKS,
    "DENVER NUGGETS": Team.DENVER_NUGGETS,
    "DETROIT PISTONS": Team.DETROIT_PISTONS,
    "GOLDEN STATE WARRIORS": Team.GOLDEN_STATE_WARRIORS,
    "HOUSTON ROCKETS": Team.HOUSTON_ROCKETS,
    "INDIANA PACERS": Team.INDIANA_PACERS,
    "LOS ANGELES CLIPPERS": Team.LOS_ANGELES_CLIPPERS,
    "LOS ANGELES LAKERS": Team.LOS_ANGELES_LAKERS,
    "MEMPHIS GRIZZLIES": Team.MEMPHIS_GRIZZLIES,
    "MIAMI HEAT": Team.MIAMI_HEAT,
    "MILWAUKEE BUCKS": Team.MILWAUKEE_BUCKS,
    "MINNESOTA TIMBERWOLVES": Team.MINNESOTA_TIMBERWOLVES,
    "NEW ORLEANS PELICANS": Team.NEW_ORLEANS_PELICANS,
    "NEW YORK KNICKS": Team.NEW_YORK_KNICKS,
    "OKLAHOMA CITY THUNDER": Team.OKLAHOMA_CITY_THUNDER,
    "ORLANDO MAGIC": Team.ORLANDO_MAGIC,
    "PHILADELPHIA 76ERS": Team.PHILADELPHIA_76ERS,
    "PHOENIX SUNS": Team.PHOENIX_SUNS,
    "PORTLAND TRAIL BLAZERS": Team.PORTLAND_TRAIL_BLAZERS,
    "SACRAMENTO KINGS": Team.SACRAMENTO_KINGS,
    "SAN ANTONIO SPURS": Team.SAN_ANTONIO_SPURS,
    "TORONTO RAPTORS": Team.TORONTO_RAPTORS,
    "UTAH JAZZ": Team.UTAH_JAZZ,
    "WASHINGTON WIZARDS": Team.WASHINGTON_WIZARDS,

    # NBA DEPRECATED TEAMS
    "ANDERSON PACKERS": Team.ANDERSON_PACKERS,
    "BALTIMORE BULLETS": Team.BALTIMORE_BULLETS,
    "BUFFALO BRAVES": Team.BUFFALO_BRAVES,
    "CAPITAL BULLETS": Team.CAPITAL_BULLETS,
    "CHARLOTTE BOBCATS": Team.CHARLOTTE_BOBCATS,
    "CHICAGO PACKERS": Team.CHICAGO_PACKERS,
    "CHICAGO STAGS": Team.CHICAGO_STAGS,
    "CHICAGO ZEPHYRS": Team.CHICAGO_ZEPHYRS,
    "CINCINNATI ROYALS": Team.CINCINNATI_ROYALS,
    "CLEVELAND REBELS": Team.CLEVELAND_REBELS,
    "DETROIT FALCONS": Team.DETROIT_FALCONS,
    "FORT WAYNE PISTONS": Team.FORT_WAYNE_PISTONS,
    "INDIANAPOLIS JETS": Team.INDIANAPOLIS_JETS,
    "INDIANAPOLIS OLYMPIANS": Team.INDIANAPOLIS_OLYMPIANS,
    "KANSAS CITY KINGS": Team.KANSAS_CITY_KINGS,
    "KANSAS CITY-OMAHA KINGS": Team.KANSAS_CITY_OMAHA_KINGS,
    "MILWAUKEE HAWKS": Team.MILWAUKEE_HAWKS,
    "MINNEAPOLIS LAKERS": Team.MINNEAPOLIS_LAKERS,
    "NEW JERSEY NETS": Team.NEW_JERSEY_NETS,
    "NEW ORLEANS HORNETS": Team.NEW_ORLEANS_HORNETS,
    "NEW ORLEANS JAZZ": Team.NEW_ORLEANS_JAZZ,
    "NEW ORLEANS/OKLAHOMA CITY HORNETS": Team.NEW_ORLEANS_OKLAHOMA_CITY_HORNETS,
    "NEW YORK NETS": Team.NEW_YORK_NETS,
    "PITTSBURGH IRONMEN": Team.PITTSBURGH_IRONMEN,
    "PHILADELPHIA WARRIORS": Team.PHILADELPHIA_WARRIORS,
    "PROVIDENCE STEAMROLLERS": Team.PROVIDENCE_STEAMROLLERS,
    "ROCHESTER ROYALS": Team.ROCHESTER_ROYALS,
    "SAN DIEGO CLIPPERS": Team.SAN_DIEGO_CLIPPERS,
    "SAN DIEGO ROCKETS": Team.SAN_DIEGO_ROCKETS,
    "SAN FRANCISCO WARRIORS": Team.SAN_FRANCISCO_WARRIORS,
    "SEATTLE SUPERSONICS": Team.SEATTLE_SUPERSONICS,
    "SHEBOYGAN RED SKINS": Team.SHEBOYGAN_RED_SKINS,
    "ST. LOUIS BOMBERS": Team.ST_LOUIS_BOMBERS,
    "ST. LOUIS HAWKS": Team.ST_LOUIS_HAWKS,
    "SYRACUSE NATIONALS": Team.SYRACUSE_NATIONALS,
    "TORONTO HUSKIES": Team.TORONTO_HUSKIES,
    "TRI-CITIES BLACKHAWKS": Team.TRI_CITIES_BLACKHAWKS,
    "VANCOUVER GRIZZLIES": Team.VANCOUVER_GRIZZLIES,
    "WASHINGTON BULLETS": Team.WASHINGTON_BULLETS,
    "WASHINGTON CAPITOLS": Team.WASHINGTON_CAPITOLS,
    "WATERLOO HAWKS": Team.WATERLOO_HAWKS,
}

SCHEDULE_COLUMN_NAMES = [
    "start_time",
    "away_team",
    "away_team_score",
    "home_team",
    "home_team_score",
]

BASE_URL = 'https://www.basketball-reference.com'


class CSVWriter:
    def __init__(self, column_names, row_formatter):
        self.column_names = column_names
        self.row_formatter = row_formatter

    def format_rows(self, data):
        return [self.row_formatter.format(row_data) for row_data in data]

    def write(self, data, options):
        with open(options.file_path, options.mode.value, newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.column_names)
            writer.writeheader()
            writer.writerows(self.format_rows(data=data))


class RowFormatter:
    def __init__(self, data_field_names):
        self.data_field_names = data_field_names

    @staticmethod
    def format_field_data(field_name, field_data):
        if field_name in [
            "away_team",
            "home_team",
            "team",
            "location",
            "opponent",
            "outcome",
            "relevant_team",
            "period_type",
            "leagues",
        ]:
            if field_data is None:
                return None
            if isinstance(field_data, set):
                return "-".join(map(lambda data: data.value, list(field_data)))
            return field_data.value
        elif field_name == "positions":
            return "-".join(map(lambda position: position.value, field_data))
        else:
            return field_data

    def format(self, row_data):
        return {
            data_field_name: self.format_field_data(
                field_name=data_field_name,
                field_data=row_data[data_field_name],
            )
            for data_field_name in self.data_field_names
        }


def str_to_int(value, default=int(0)):
    stripped_value = value.strip()
    try:
        return int(stripped_value)
    except ValueError:
        return default


class SchedulePage:
    def __init__(self, html):
        self.html = html

    @property
    def other_months_schedule_links_query(self):
        return '//div[@id="content"]' \
               '/div[@class="filter"]' \
               '/div[not(contains(@class, "current"))]' \
               '/a'

    @property
    def rows_query(self):
        return '//table[@id="schedule"]//tbody/tr'

    @property
    def other_months_schedule_urls(self):
        links = self.html.xpath(self.other_months_schedule_links_query)
        return [
            link.attrib['href']
            for link in links
        ]

    @property
    def rows(self):
        return [
            ScheduleRow(html=row)
            for row in self.html.xpath(self.rows_query)
            # Every row in each month's schedule table represents a game
            # except for the row where the only content is "Playoffs"
            if row.text_content() != 'Playoffs'
        ]


class ScheduleRow:
    def __init__(self, html):
        self.html = html

    def __eq__(self, other):
        if isinstance(other, ScheduleRow):
            return self.html == other.html
        return False

    @property
    def start_date(self):
        cells = self.html.xpath('th[@data-stat="date_game"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def start_time_of_day(self):
        cells = self.html.xpath('td[@data-stat="game_start_time"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def away_team_name(self):
        cells = self.html.xpath('td[@data-stat="visitor_team_name"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def home_team_name(self):
        cells = self.html.xpath('td[@data-stat="home_team_name"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def away_team_score(self):
        cells = self.html.xpath('td[@data-stat="visitor_pts"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''

    @property
    def home_team_score(self):
        cells = self.html.xpath('td[@data-stat="home_pts"]')

        if len(cells) > 0:
            return cells[0].text_content()

        return ''


class ScheduledGamesParser:
    def __init__(self, start_time_parser, team_name_parser):
        self.start_time_parser = start_time_parser
        self.team_name_parser = team_name_parser

    def parse_games(self, games):
        return [
            {
                "start_time": self.start_time_parser.parse_start_time(
                    formatted_date=game.start_date,
                    formatted_time_of_day=game.start_time_of_day,
                ),
                "away_team": self.team_name_parser.parse_team_name(team_name=game.away_team_name),
                "home_team": self.team_name_parser.parse_team_name(team_name=game.home_team_name),
                "away_team_score": str_to_int(value=game.away_team_score, default=None),
                "home_team_score": str_to_int(value=game.home_team_score, default=None),
            }
            for game in games
        ]


class TeamNameParser:
    def __init__(self, team_names_to_teams):
        self.team_names_to_teams = team_names_to_teams

    def parse_team_name(self, team_name):
        return self.team_names_to_teams[team_name.strip().upper()]


class ScheduledStartTimeParser:
    def __init__(self, time_zone=pytz.utc):
        self.time_zone = time_zone

    def parse_start_time(self, formatted_date, formatted_time_of_day):
        if formatted_time_of_day is not None and formatted_time_of_day not in ["", " "]:
            # Starting in 2018, the start times had a "p" or "a" appended to the end
            # Between 2001 and 2017, the start times had a "pm" or "am"
            #
            # https://www.basketball-reference.com/leagues/NBA_2018_games.html
            # vs.
            # https://www.basketball-reference.com/leagues/NBA_2001_games.html
            is_prior_format = formatted_time_of_day[-2:] == "am" or formatted_time_of_day[-2:] == "pm"

            # If format contains only "p" or "a" add an "m" so it can be parsed by datetime module
            if is_prior_format:
                combined_formatted_time = formatted_date + " " + formatted_time_of_day
            else:
                combined_formatted_time = formatted_date + " " + formatted_time_of_day + "m"

            if is_prior_format:
                start_time = datetime.strptime(combined_formatted_time, "%a, %b %d, %Y %I:%M %p")
            else:
                start_time = datetime.strptime(combined_formatted_time, "%a, %b %d, %Y %I:%M%p")
        else:
            start_time = datetime.strptime(formatted_date, "%a, %b %d, %Y")

        # All basketball reference times seem to be in Eastern
        est = pytz.timezone("US/Eastern")
        localized_start_time = est.localize(start_time)
        return localized_start_time.astimezone(self.time_zone)


def schedule_for_month(url):
    response = requests.get(url=url)

    response.raise_for_status()

    page = SchedulePage(html=html.fromstring(html=response.content))
    parser = ScheduledGamesParser(
        start_time_parser=ScheduledStartTimeParser(),
        team_name_parser=TeamNameParser(team_names_to_teams=TEAM_NAME_TO_TEAM),
    )
    return parser.parse_games(games=page.rows)


def get_season_schedule(season_year, league=WNBA):
    if league == WNBA:
        url = '{BASE_URL}/wnba/years/{season_year}-schedule.html'.format(
            BASE_URL=BASE_URL,
            season_year=season_year
        )
    elif league == NBA:
        if season_year <= 1949:
            league = BAA
        url = '{BASE_URL}/leagues/{league}_{season_year}_games.html'.format(
            BASE_URL=BASE_URL,
            league=league,
            season_year=season_year
        )


    response = requests.get(url=url)
    response.raise_for_status()

    page = SchedulePage(html=html.fromstring(html=response.content))
    parser = ScheduledGamesParser(
        start_time_parser=ScheduledStartTimeParser(),
        team_name_parser=TeamNameParser(team_names_to_teams=TEAM_NAME_TO_TEAM),
    )
    season_schedule_values = parser.parse_games(games=page.rows)

    if league in [BAA, NBA]:
        for month_url_path in page.other_months_schedule_urls:
            url = '{BASE_URL}{month_url_path}'.format(BASE_URL=BASE_URL, month_url_path=month_url_path)
            monthly_schedule = schedule_for_month(url=url)
            season_schedule_values.extend(monthly_schedule)
    return season_schedule_values


class PlayoffPage:
    def __init__(self, html):
        self.html = html

    @property
    def championship_team_query(self):
        return '//p'

    @property
    def championship_team(self):
        query_elements = self.html.xpath(self.championship_team_query)
        for elem in query_elements:
            content = elem.text_content()
            if "League Champion" in content:
                championship_team = content.split(":")[1].strip()
                return championship_team
        return None
    

def get_correct_team_name(team, year, league):
    if league == NBA or league == BAA:
        if team == 'Seattle SuperSonics':
            return 'Seattle Supersonics'
        if team == 'New Orleans/Oklahoma City Hornets':
            return 'New Orleans Hornets'
        if team == 'Sheboygan Red Skins':
            return 'Sheboygan R-- S----'
        if team == 'Charlotte Hornets' and year <= 2002:
            return 'Charlotte Hornets (Original)'
        if team == 'Baltimore Bullets' and year <= 1954:
            return 'Baltimore Bullets (Original)'
        if team == 'Denver Nuggets' and year == 1950:
            return 'Denver Nuggets (Original)'
    return team


def get_championship_team(season_year, league=WNBA):
    if league == WNBA:
        url = '{BASE_URL}/wnba/years/{season_year}-schedule.html'.format(
            BASE_URL=BASE_URL,
            season_year=season_year
        )
    elif league == NBA:
        if season_year <= 1949:
            league = BAA
        url = '{BASE_URL}/playoffs/{league}_{season_year}.html'.format(
            BASE_URL=BASE_URL,
            league=league,
            season_year=season_year
        )

    response = requests.get(url=url)
    response.raise_for_status()
    if league == WNBA:
        page = SchedulePage(html=html.fromstring(html=response.content))
        last_game = page.rows[-1]
        home_team = last_game.home_team_name
        away_team = last_game.away_team_name
        home_score = int(last_game.home_team_score)
        away_score = int(last_game.away_team_score)
        if home_score > away_score:
            return get_correct_team_name(home_team, season_year, league)
        else:
            return get_correct_team_name(away_team, season_year, league)
    else:
        page = PlayoffPage(html=html.fromstring(html=response.content))
        team = get_correct_team_name(page.championship_team, season_year, league)
        return team
