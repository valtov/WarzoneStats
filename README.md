# WarzoneStats

WarzoneStats is a Python wrapper for the COD Warzone Api (https://documenter.getpostman.com/view/5519582/SzzgAefq). There is an additional wrapper for the https://wzstats.gg/ website. There are also some helpful functions to extract useful data from the api responses.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install WarzoneStats.

```bash
pip3 install WarzoneStats
```

## Usage

Before using the COD Api you first need to login to [Activision](https://www.activision.com/) and get the ACT\_SSO\_COOKIE

You can do this in Chrome by going into inspect element -\> Application tab -\> Cookies -\> enter ACT\_SSO\_COOKIE into the filter field

Copy and save this value to use in the package

**You should be caching the return values from both Api and ApiGG so you don't keep sending the same request and end up getting ip banned**
 
### COD Api
```python
from WarzoneStats import Api

username = 'huskerrs#1343'

# Can see the platform values by referencing Api.Platforms
platform = 'battle' 

sso = 'Get this value from the ACT_SSO_COOKIE that is set in Chrome by logging into activision.com'

api = Api(username, platform, sso)

# You can view all sample responses in the Sample Endpoint Responses Folder

# This endpoint returns lifetime stats like kd, gun accuracy, weekly stats, etc
profile = api.get_profile()
print(profile['data']['lifetime']['all']['properties']['kdRation'])

# This endpoint returns 20 recent matches with everything from team name, team placement to the loadouts everyone used
recentMatches = api.get_recentMatches()	
print(recentMatches['data']['summary']['all']['kills'])

# Returns 1000 recent matches, with only the timestamps, matchIds, mapId, and platform
# Useful for using matchIds to get stats of that match (lobby kd etc)
matches = api.get_matches()
matchId = recentMatches['data'][0]['matchId']
print(matchId)

# Returns the details of the specific match per player; each players stats from the loadout they used to the kills they got is listed
matchDetails = api.get_matchDetails(matchId)
print(matchDetails['data']['allPlayers'][0]['player']['username'])
```

### wzstats.gg
```python
from WarzoneStats import ApiGG

username = 'nrg joewo#2631118'
platform = 'acti'

api = ApiGG()

stats = api.get_stats(username, platform)
print(stats)
```

### parser
```python
from WarzoneStats import ApiGG, ParserGG

username = 'nrg joewo#2631118'
platform = 'acti'

api = ApiGG()

stats = api.get_stats(username, platform)

parser = ParserGG()

print(parser.get_average_kd_lobbies(stats))

''' and '''

# Get this from either Api or ApiGG response
match_id = '6702851451945654660'

match = api.get_match(match_id)

print(parser.get_average_lobby_kd(match)


```

## License
[MIT](https://choosealicense.com/licenses/mit/)
