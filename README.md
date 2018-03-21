# Sportmonks Api

Unnoficial Api to retrieve soccer data from [Sportmonks](https://sportmonks.com/)

Example:
```python
import sportmonks_calls as sm

#load features class
fixtures = sm.Fixtures(sportmonks_token)

#query all fixtures by specific date
fixture_date = '2017-10-10'
fixtures.by_date(fixture_date)

print (fixture.request.results)

[{'aggregate_id': None,
  'attendance': None,
  'coaches': {'localteam_coach_id': None, 'visitorteam_coach_id': None},
  'commentaries': True,
  'deleted': False,
  'formations': {'localteam_formation': '4-4-2',
   'visitorteam_formation': '4-2-3-1'},
  'group_id': None,
  'id': 236705,
  'league_id': 720,
  'localteam_id': 18701,
  'pitch': None,
  'referee_id': 3,
  'round_id': 28849,
  'scores': {'et_score': None,
   'ft_score': '2-0',
   'ht_score': '1-0',
   'localteam_pen_score': None,
   'localteam_score': 2,
   'visitorteam_pen_score': None,
   'visitorteam_score': 0},
  'season_id': 898,
  'stage_id': 1753,
  'standings': {'localteam_position': 2, 'visitorteam_position': 1},
  'time': {'added_time': None,
   'extra_minute': None,
   'injury_time': 3,
   'minute': 90,
   'second': None,
   'starting_at': {'date': '2017-10-10',
    'date_time': '2017-10-10 18:45:00',
    'time': '18:45:00',
    'timestamp': 1507661100,
    'timezone': 'UTC'},
   'status': 'FT'},
  'venue_id': 8412,
  'visitorteam_id': 18708,
  'weather_report': None,
  'winning_odds_calculated': True}]
```
