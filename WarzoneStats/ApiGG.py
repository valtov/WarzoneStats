import requests

class ApiGG:
    headers = {
        'authority': 'app.wzstats.gg',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'if-none-match': 'W/"23ef-cdBmgtEtsALv7M0AnmO49iBAx80"',
        'origin': 'https://wzstats.gg',
        'referer': 'https://wzstats.gg/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    }
    
    def __init__(self):
        pass
    
    def get_stats(self, username, platform, skip=True):
        platforms = ['battle', 'xbl', 'psn', 'acti']
        
        if platform not in platforms:
            print(f'Platform {platform} invalid. Must be one of {platforms}')
            return None
        
        params = {
            'username': username,
            'platform': platform,
        }

        response = requests.get('https://app.wzstats.gg/v2/player/match/withPlayers/', params=params, headers=ApiGG.headers)
        if response.status_code > 299:
            print(f'Response code: [{response.status_code}]\n\n{response.text}')
            return None
        else:
            stats = response.json()
            if skip:
                return stats
            # If a match has not been loaded on wzstats.gg yet, it will not have the matchStatData field
            # This goes one by one through every match to check if it has the matchStatData field and if
            # it doesnt, it makes another call to wzstats to get the full data on that match and fills in
            # he matchStatData field. This functionality is turned off by default
            else:
                for i, match in enumerate(stats['matches']):
                    if 'matchStatData' not in match:
                        try:
                            id = match['id']
                            full_match = self.get_match(id)
                            stats['matches'][i]['matchStatData'] = full_match['matchStatData']
                        except:
                            continue
                return stats

    def get_match(self, match_id):
        params = {
            'matchId': match_id,
        }

        response = requests.get('https://app.wzstats.gg/v2/', params=params, headers=ApiGG.headers)
        if response.status_code > 299:
            print(f'Response code: [{response.status_code}]\n\n{response.text}')
            return None
        else:
            return response.json()

if __name__ == '__main__':
    username = 'nrg joewo#2631118'
    platform = 'acti'

    api = ApiGG()
    stats = api.get_stats(username, platform)
    print(stats)