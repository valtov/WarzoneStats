import urllib.parse
import requests
from enum import Enum

class Api:
    xsrf = '68e8b62e-1d9d-4ce1-b93f-cbe5ff31a041'
    base_cookie = 'new_SiteId=cod; ACT_SSO_LOCALE=en_US;country=US;'
    cookie = '{base_cookie}ACT_SSO_COOKIE={sso};XSRF-TOKEN={xsrf};API_CSRF_TOKEN={xsrf};ACT_SSO_EVENT="LOGIN_SUCCESS:1644346543228";ACT_SSO_COOKIE_EXPIRY=1645556143194;comid=cod;ssoDevId=63025d09c69f47dfa2b8d5520b5b73e4;tfa_enrollment_seen=true;gtm.custom.bot.flag=human;'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Content-Type': 'application/json',
        'X-XSRF-TOKEN': xsrf,
        'X-CSRF-TOKEN': xsrf,
        'Atvi-Auth': None,
        'ACT_SSO_COOKIE': None,
        'atkn': None,
        'cookie': None
    }
    baseUrl = 'https://my.callofduty.com/api/papi-client'

    class Platforms(Enum):
        PSN = 'psn'
        XBOX = 'xbl'
        BATTLENET = 'battle'
        ACTIVISION = 'uno'

    class Endpoints(Enum):
        # Lists lifetime stats like kd, gun accuracy etc, as well as weekly stats separated by all gamemodes played that week
        profile = '/stats/cod/v1/title/mw/platform/{platform}/{endpointType}/{username}/profile/type/wz'
        # Returns 20 recent matches with everything from team name, team placement to the loadouts everyone used, as well as a summary of your own stats for those matches
        recentMatches = '/crm/cod/v2/title/mw/platform/{platform}/{endpointType}/{username}/matches/wz/start/0/end/0/details'
        # Returns 1000 recent matches, with only the timestamps, matchIds, mapId, and platform
        matches = '/crm/cod/v2/title/mw/platform/{platform}/{endpointType}/{username}/matches/wz/start/0/end/0'
        # Returns the details of the specific match per player; each players stats from the loadout they used to the kills they got is listed
        matchDetails = '/crm/cod/v2/title/mw/platform/{platform}/fullMatch/wz/{matchId}/en'

    def __init__(self, username, platform, ssoCookie):
        plats = set(item.value for item in Api.Platforms)
        if platform not in plats:
            raise ValueError(f'Platform type {platform} does not exist. Must be one of {plats}')
        if platform == Api.Platforms.ACTIVISION:
            self.endpointType = 'uno'
        else:
            self.endpointType = 'gamer'
        self.platform = platform
        self.login(username, ssoCookie)

    def login(self, username, ssoCookie):
        self.username = Api._convert_username(username)
        self.ssoCookie = ssoCookie
        self.headers = Api.headers
        self.headers['Atvi-Auth'] = ssoCookie
        self.headers['ACT_SSO_COOKIE'] = ssoCookie
        self.headers['atkn'] = ssoCookie
        self.headers['cookie'] = Api.cookie.format(base_cookie=Api.base_cookie,sso=ssoCookie,xsrf=Api.xsrf)
        self.loggedIn = True
    
    def get_profile(self):
        url = Api.baseUrl + Api.Endpoints.profile.format(platform=self.platform, endpointType=self.endpointType, username=self.username)
        r = requests.get(url, headers=self.headers)
        if r.status_code > 299:
            self.loggedIn = False
            print(f'Request error occured, returned status code {r.status_code}.\n{r.text}\nMost likely incorrect ssoCookie or username. Relogin and try again.')
        return r.json()

    def get_recentMatches(self):
        url = Api.baseUrl + Api.Endpoints.recentMatches.format(platform=self.platform, endpointType=self.endpointType, username=self.username)
        r = requests.get(url, headers=self.headers)
        if r.status_code > 299:
            self.loggedIn = False
            print(f'Request error occured, returned status code {r.status_code}.\n{r.text}\nMost likely incorrect ssoCookie or username. Relogin and try again.')
        return r.json()
    
    def get_matches(self):
        url = Api.baseUrl + Api.Endpoints.matches.format(platform=self.platform, endpointType=self.endpointType, username=self.username)
        r = requests.get(url, headers=self.headers)
        if r.status_code > 299:
            self.loggedIn = False
            print(f'Request error occured, returned status code {r.status_code}.\n{r.text}\nMost likely incorrect ssoCookie or username. Relogin and try again.')
        return r.json()
    
    def get_matchDetails(self, matchId):
        url = Api.baseUrl + Api.Endpoints.matchDetails.format(platform=self.platform, matchId=matchId)
        r = requests.get(url, headers=self.headers)
        if r.status_code > 299:
            print(f'Request error occured, returned status code {r.status_code}.\n{r.text}\nMost likely matchId is invalid.')
        return r.json()
    
    def _convert_username(self, username):
        return urllib.parse.quote(username)
