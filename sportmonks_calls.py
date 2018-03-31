#!/usr/bin/python

import requests
import json
import time
from collections import OrderedDict###### LIST OF ENDPOINTS FROM SPORTMONKS #######################################
'''
// Continents
// Countries
// Leagues
// Seasons
// Fixtures
// Livescores
// Commentaries
// Video Highlights
// Head2Head
// TVStations
// Standings
// Teams
// Topscorers
// Venues
// Rounds
// Pre-Match-Odds
// In-Play-Odds
// Players
// Bookmakers
// Team-Squads
'''
#### maybe i need to map all the includes for proper parsing

includes = {
    "visitorTeam": ['country_id','founded','id', 'legacy_id','logo_path','name','national_team','twitter','venue_id'],
    "localTeam": ['country_id','founded','id', 'legacy_id','logo_path','name','national_team','twitter','venue_id'],
    "goals": ['extra_minute','fixture_id','id','minute','player_assist_id','player_assist_name','player_id','player_name','result','team_id','type'],
    "stats": ['attacks','corners','fixture_id','fouls','free_kick','goal_kick','offsides','passes','possessiontime','redcards','saves','shots','substitutions','team_id','throw_in','yellowcards'],
    "corners": ['comment','extra_minute','fixture_id','id','minute','team_id'],
    "bench": ['additional_position','fixture_id','formation_position','number','player_id','player_name','position','posx','posy','stats','team_id'],
    "localCoach": [],
    "visitorCoach": [],
    "group": [],
    "groups": [],
    "odds": [],
    "venue": [],
    "events": [],
    "referee": [],
    "stage": [],
    "round": ['end','id','league_id','name','season_id','stage_id','start'],
    "season": ['current_round_id','current_stage_id','id','is_current_season','league_id','name'],
    "league": [],
    "highlights": [],
    "tvstations": [],
    "comments": [],
    "sidelined": [],
    "lineup": [],
    "other": [],
    "cards": [],
    "substitutions": [],
    "inplay": [],
    "flatOdds": [],
    "coach": [],
    "squad": [],
    "transfers": [],
    "fifaranking": [],
    "uefaranking": [],
    "visitorFixtures": [],
    "localFixtures": [],
    "latest": [],
    "upcoming": [],
    "visitorResults": [],
    "localResults": [],
    "fixtures": [],
    "fixture": [],
    "results": []
}


################################################################################
####debug-global-var############################################################

http = 'https://soccer.sportmonks.com/api/v2.0'

DEBUG_MODE = False

token_path = ''

with open('{0}/settings.json'.format(token_path)) as json_data:
    settings = json.load(json_data)

sportmonks_token = settings['sportmonks']['api_token']

################################################################################

#global class to call SporMonks API
class Spms(object):
    """
    General sportmonks request class
    --------------------------------------
        Methods Available:
        | make_request()
    """

    def __init__(self, token='', include = ''):
        """
        parameters :
        ------------
            | token: sportmonks token
            | include: string with all includes for the API request
        """
        self.token = token
        self.include = include
        self.api_calls = 0

    def make_request(self, endpoint, paginated = False, verbose=DEBUG_MODE):
        """
        parameters :
        ------------
            | endpoint: endpoint for the request
            | paginated: boolean. View documentation for more info
            | verbose: boolean
        """
        #if paginated = true, then make sure to loop through all pages
        self.payload = {'api_token': self.token,
            'Accept': 'application/json',
            'page': 1,
            'include': self.include}

        if not paginated:

            request = requests.get(endpoint, params=self.payload)
            self.api_calls += 1
            [print (self.api_calls) if verbose else None]

            if request.status_code != 200:
                fixture_results = {'data':'Error'}
                return False
            else:
                fixture_results = request.json()['data']
        else:
            first_request = requests.get(endpoint, params=self.payload)
            meta = first_request.json()
            pages = meta['meta']['pagination']['total_pages']

            fixture_results = []
            for page in range(1,pages,1):
                self.payload['page'] = page

                [time.sleep(2.4) if int(pages) >  1500 else None]
                [print (self.api_calls) if verbose else None]

                request = requests.get(endpoint, params=self.payload)
                self.api_calls += 1

                fixtures = request.json()
                for fixture in fixtures['data']:
                    fixture_results.append(fixture)

        self.results = fixture_results

        return True

################################################################################

class Livescores(object):
    """
        Class to query livescores
        -------------------------
            Methods Available:
            | get_all()
            | get_all_today()
    """
    endpoint = http + '/livescores'
    includes = {
        "get_all": "localTeam,visitorTeam,substitutions,goals,cards,other,corners,\
            lineup,bench,sidelined,stats,comments,tvstations,highlights,\
            league,season,round,stage,referee,events,venue,odds,flatOdds,\
            inplay,localCoach,visitorCoach,group",
        "get_all_today": "localTeam,visitorTeam,substitutions,goals,cards,other\
            ,corners,lineup,bench,sidelined,stats,comments,tvstations,highlights,\
            league,season,round,stage,referee,events,venue,odds,inplay,\
            localCoach,visitorCoach,group"
            }
    includes_limit = {"get_all": 10, "get_all_today": 10}

    def __init__(self, token, include = ''):
        self.request = Spms(token = token, include=include)

    def get_all(self, include = ''):
        http_request = self.endpoint +'/now'
        self.request.include = include
        self.request.make_request(http_request, paginated = False)
        return True

    def get_all_today(self, include = ''):
        http_request = self.endpoint
        self.request.include = include
        self.request.make_request(http_request, paginated = True)
        return True

class Fixtures(object):

    endpoint = http + '/fixtures'
    includes = {
        "by_range": "localTeam, visitorTeam, substitutions, goals, cards, \
            other, corners, lineup, bench, sidelined, stats, comments, tvstations, \
            highlights, league, season, round, stage, referee, events, venue, odds, \
            flatOdds, inplay, localCoach, visitorCoach,group",
        "by_id": "localTeam, visitorTeam, substitutions, goals, cards, other, corners,\
            lineup, bench, sidelined, stats, comments, tvstations, highlights, league, \
            season, round, stage, referee, events, venue, odds, flatOdds, inplay, \
            localCoach, visitorCoach,group",
        "by_date": "localTeam, visitorTeam, substitutions, goals, cards, other, corners,\
            lineup, bench, sidelined, stats, comments, tvstations, highlights, league, season,\
             round, stage, referee, events, venue, odds, flatOdds, inplay, localCoach, \
             visitorCoach,group"
             }
    includes_limit = {"by_range": 3, "by_id": 3, "by_date": 3}

    def __init__(self, token, include=''):
        self.request = Spms(token = token, include=include)

    def by_range(self, date_start, date_end, include=''):
        self.request.include = include
        http_request =  self.endpoint + '/between/{0}/{1}'.format(date_start, date_end)
        self.request.make_request(http_request, paginated = True)
        return True

    def by_id(self, fixture_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/{0}'.format(fixture_id)
        self.request.make_request(http_request, paginated = False)
        return True

    def by_date(self, fixture_date, include=''):
        self.request.include = include
        http_request = self.endpoint + '/date/{0}'.format(fixture_date)
        self.request.make_request(http_request, paginated = True)
        return True


class Pre_Match_Odds(object):

    endpoint = http + '/odds'
    includes = {
        "by_fixture": "",
        "by_fixture_bookmaker": "",
        "by_fixture_market": ""
        }
    includes_limit = {"by_fixture": 0, "by_fixture_bookmaker": 0, "by_fixture_market": 0}

    def __init__(self, token):
        self.request = Spms(token = token, include='')

    def by_fixture(self, fixture_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/fixture/{0}'.format(fixture_id)
        self.request.make_request(http_request, paginated = False)
        return True

    def by_fixture_bookmaker(self, fixture_id, bookmaker_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/{0}/bookmaker/{1}'.format(fixture_id, bookmaker_id)
        self.request.make_request(http_request, paginated = False)
        return True

    def by_fixture_market(self, fixture_id, market_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/{0}/market/{1}'.format(fixture_id, market_id)
        self.request.make_request(http_request, paginated = False)
        return True


class Continents(object):

    endpoint = http + '/continents'
    includes = {
        "get_all": "countries",
        "by_id": "countries"
        }
    includes_limit = {"get_all": 10, "by_id": 10}

    def __init__(self, token, include=''):
        self.request = Spms(token = token, include = '')

    def get_all(self, include=''):
        self.request.include = include
        http_request = self.endpoint
        self.request.make_request(http_request, paginated = False)
        return True

    def by_id(self, continent_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/{0}'.format(continent_id)
        self.request.make_request(http_request, paginated = False)
        return True


class Countries(object):

    endpoint = http + '/countries'
    includes = {
        "get_all": "continent,leagues",
        "by_id": "continent,leagues"
        }
    includes_limit = {"get_all": 2, "by_id": 2}

    def __init__(self, token, include=''):
        self.request = Spms(token = token, include = '')

    def get_all(self, include=''):
        self.request.include = include
        http_request = self.endpoint
        self.request.make_request(http_request, paginated = True)
        return True

    def by_id(self, country_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/{0}'.format(country_id)
        self.request.make_request(http_request, paginated = False)
        return True


class Leagues(object):

    endpoint = http + '/leagues'
    includes = {
        "get_all": "countries,seasons,season",
        "by_id": "countries,seasons,season"
        }
    includes_limit = {"get_all": 2, "by_id": 10}

    def __init__(self, token, include=''):
        self.request = Spms(token = token, include = '')

    def get_all(self, include=''):
        self.request.include = include
        http_request = self.endpoint
        self.request.make_request(http_request, paginated = True)
        return True

    def by_id(self, league_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/{0}'.format(league_id)
        self.request.make_request(http_request, paginated = False)
        return True


class Seasons(object):

    endpoint = http + '/seasons'
    includes = {
        "get_all": "league,stages,rounds,fixtures,upcoming,results,groups",
        "by_id": "league,stages,rounds,fixtures,upcoming,results,groups"
        }
    includes_limit = {"get_all": 2, "by_id": 10}

    def __init__(self, token, include=''):
        self.request = Spms(token = token, include = '')

    def get_all(self, include=''):
        self.request.include = include
        http_request = self.endpoint
        self.request.make_request(http_request, paginated = True)
        return True

    def by_id(self, season_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/{0}'.format(season_id)
        self.request.make_request(http_request, paginated = False)
        return True


class Commentaries(object):

    endpoint = http + '/commentaries'
    includes = {
        "by_fixture": ""
        }
    includes_limit = {"by_fixture": 0}

    def __init__(self, token, include=''):
        self.request = Spms(token = token, include = '')

    def by_fixture(self, fixture_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/fixture/{0}'.format(fixture_id)
        self.request.make_request(http_request, paginated = False)
        return True


class Videos(object):

    endpoint = http + '/highlights'
    includes = {
        "get_all":"fixture",
        "by_fixture": ""
        }
    includes_limit = {"get_all":2,"by_fixture": 0}

    def __init__(self, token, include=''):
        self.request = Spms(token = token, include = '')

    def get_all(self, include=''):
        self.request.include = include
        http_request = self.endpoint
        self.request.make_request(http_request, paginated = True)
        return True

    def by_fixture(self, fixture_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/fixture/{0}'.format(fixture_id)
        self.request.make_request(http_request, paginated = False)
        return True


class Head2Head(object):

    endpoint = http + '/head2head'
    includes = {
        "by_teams":"localTeam,visitorTeam,substitutions,goals,cards,other,lineup,\
         bench,stats,comments,tvstations,highlights,league,season,round,stage,referee,\
         events,venue"
        }
    includes_limit = {"by_teams":2}

    def __init__(self, token, include=''):
        self.request = Spms(token = token, include = '')

    def by_teams(self, team1_id, team2_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/{0}/{1}'.format(team1_id, team2_id)
        self.request.make_request(http_request, paginated = False)
        return True


class TVStations(object):

    endpoint = http + '/tvstations'
    includes = {
        "by_fixture":""
        }
    includes_limit = {"by_fixture":0}

    def __init__(self, token, include=''):
        self.request = Spms(token = token, include = '')

    def by_fixture(self, fixture_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/fixture/{0}'.format(fixture_id)
        self.request.make_request(http_request, paginated = False)
        return True


class Standings(object):

    endpoint = http + '/standings'
    includes = {
        "by_season":"team,league,season,round,stage",
        "live_by_season":"team,league,season,round,stage"
        }
    includes_limit = {"by_season":2,"live_by_season":2}

    def __init__(self, token, include=''):
        self.request = Spms(token = token, include = '')

    def by_season(self, season_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/season/{0}'.format(season_id)
        self.request.make_request(http_request, paginated = False)
        return True

    def live_by_season(self, season_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/season/live/{0}'.format(season_id)
        self.request.make_request(http_request, paginated = False)
        return True


class Teams(object):

    endpoint = http + '/teams'
    includes = {
        "by_id":"country,squad,coach,transfers,sidelined,stats,venue,fifaranking,\
            uefaranking,visitorFixtures,localFixtures,visitorResults,localResults,\
            latest,upcoming",
        "by_season":"country,squad,coach,transfers,sidelined,stats,venue,fifaranking,\
            uefaranking,visitorFixtures,localFixtures,visitorResults,localResults,\
            latest,upcoming"
        }
    includes_limit = {"by_id":3,"by_season":3}

    def __init__(self, token, include=''):
        self.request = Spms(token = token, include = '')

    def by_id(self, team_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/{0}'.format(team_id)
        self.request.make_request(http_request, paginated = False)
        return True

    def by_season(self, season_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/season/{0}'.format(season_id)
        self.request.make_request(http_request, paginated = False)
        return True


class Topscorers(object):

    endpoint = http + '/topscorers'
    includes = {
        "by_season":"goalscorers.player,goalscorers.team"
        }
    includes_limit = {"by_season":3}

    def __init__(self, token, include=''):
        self.request = Spms(token = token, include = '')

    def by_season(self, season_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/season/{0}'.format(season_id)
        self.request.make_request(http_request, paginated = False)
        return True


class Venues(object):

    endpoint = http + '/venues'
    includes = {
        "by_id":""
        }
    includes_limit = {"by_id":0}

    def __init__(self, token, include=''):
        self.request = Spms(token = token, include = '')

    def by_id(self, venue_id, include=''):
        self.request.include = include
        http_request = self.endpoint+'/{0}'.format(venue_id)
        self.request.make_request(http_request, paginated = False)
        return True


class Rounds(object):

    endpoint = http + '/rounds'
    includes = {
        "by_season":"fixtures,results,season,league",
        "by_id":"fixtures,season,league"
        }
    includes_limit = {"by_season":2,"by_id":2}

    def __init__(self, token, include=''):
        self.request = Spms(token = token, include = '')

    def by_season(self, season_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/season/{0}'.format(season_id)
        self.request.make_request(http_request, paginated = False)
        return True

    def by_id(self, round_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/{0}'.format(round_id)
        self.request.make_request(http_request, paginated = False)
        return True


class In_Play_Odds(object):
    #coming from bet365

    endpoint = http + '/odds/inplay'
    includes = {
        "by_fixture":""
        }
    includes_limit = {"by_fixture":0}

    def __init__(self, token, include=''):
        self.request = Spms(token = token, include = '')

    def by_fixture(self, fixture_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/fixture/{0}'.format(fixture_id)
        self.request.make_request(http_request, paginated = False)
        return True


class Players(object):

    endpoint = http + '/players'
    includes = {
        "by_id":"position,team,stats,trophies.seasons,sidelined,transfers"
        }
    includes_limit = {"by_id":2}

    def __init__(self, token, include=''):
        self.request = Spms(token = token, include = '')

    def by_id(self, player_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/{0}'.format(player_id)
        self.request.make_request(http_request, paginated = False)
        return True


class Bookmakers(object):

    endpoint = http + '/bookmakers'
    includes = {
        "get_all":"",
        "by_id":""
        }
    includes_limit = {"get_all":0,"by_id":0}

    def __init__(self, token, include=''):
        self.request = Spms(token = token, include = '')

    def get_all(self, include=''):
        self.request.include = include
        http_request = self.endpoint
        self.request.make_request(http_request, paginated = False)
        return True

    def by_id(self, bookmaker_id, include=''):
        self.request.include = include
        http_request = self.endpoint + '/{0}'.format(bookmaker_id)
        self.request.make_request(http_request, paginated = False)
        return True


class Team_Squads(object):

    endpoint = http + '/squad'
    includes = {
        "by_team_season":"player,position"
        }
    includes_limit = {"by_team_season":3}

    def __init__(self, token, include=''):
        self.request = Spms(token = token, include = '')

    def by_team_season(self, season_id, team_id ,include =''):
        self.request.include = include
        http_request = self.endpoint + '/season/{0}/team/{1}'.format(season_id, team_id)
        self.request.make_request(http_request, paginated = False)
        return True


if __name__ == '__main__':
    livescores = Livescores(sportmonks_token)
    fixtures = Fixtures(sportmonks_token)
    pre_match_odds = Pre_Match_Odds(sportmonks_token)
    continents = Continents(sportmonks_token)
    countries = Countries(sportmonks_token)
    leagues = Leagues(sportmonks_token)
    seasons = Seasons(sportmonks_token)
    commentaries = Commentaries(sportmonks_token)
    videos = Videos(sportmonks_token)
    head2head = Head2Head(sportmonks_token)
    tvstations = TVStations(sportmonks_token)
    standings = Standings(sportmonks_token)
    teams = Teams(sportmonks_token)
    topscorers = Topscorers(sportmonks_token)
    venues = Venues(sportmonks_token)
    rounds = Rounds(sportmonks_token)
    in_play_odds = In_Play_Odds(sportmonks_token)
    players = Players(sportmonks_token)
    bookmakers = Bookmakers(sportmonks_token)
    team_squads = Team_Squads(sportmonks_token)
