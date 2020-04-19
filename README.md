# Overview
The `seasons_parser.py` file uses cherry-picked and edited code forked from (basketball-reference-web-scraper)[https://github.com/jaebradley/basketball_reference_web_scraper] repo. This version focuses only on gathering regular season team data and championship data (but no playoff data). It extends functionality to deal with all WNBA seasons and pre 1999-00 NBA seasons, extending to 1946-47 when it was the BAA. 

The `seasons.py` outputs a CSV for every season, tracking a game's result, date, and team record at the time.

The `recordigami.py` file outputs a few essential files to be used in creating data visualizations.


# Download Season Data
## WNBA
Download all WNBA seasons beginning with the 1996-1997 season.
```bash
python3 seasons.py --league WNBA
```

Script `start` and `end` arguments take in the season's end year (e.g. to refer to the 2004-05 season, use 2005). So you can download a specific season range using the following:
```bash
python3 seasons.py --league WNBA --start 2002 --end 2010
```

## NBA
Uses the same structure as above for all seasons beginning with the 1946-47 season.
```bash
python3 seasons.py --league NBA
```

And the same parameters for custom start and years.
```bash
python3 seasons.py --league NBA --start 2002 --end 2010
```