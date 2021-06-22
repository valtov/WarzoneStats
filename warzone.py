import urllib.parse
import json
import requests
import statistics
import heapq

class WarzoneTracker:

    headers = {
        'authority': 'api.tracker.gg',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': '__cfduid=da33e6ee048785828f223ee2a65b3e78d1617577303; X-Mapping-Server=s8; __cflb=02DiuFQAkRrzD1P1mdm8JatZXtAyjoPD2o7G16pDofmnL',
    }

    def __init__(self):
        # .format(username_of_battlenet)
        self.overview = 'https://api.tracker.gg/api/v2/warzone/standard/profile/battlenet/{}/'
        self.matches = 'https://api.tracker.gg/api/v2/warzone/standard/matches/battlenet/{}?type=wz'
        self.matches_next = 'https://api.tracker.gg/api/v2/warzone/standard/matches/battlenet/{}?type=wz&next={}'
        self.match_info = 'https://api.tracker.gg/api/v2/warzone/standard/matches/{}'

    def get_overview(self, player_username):
        endpoint = self.overview.format(
            self._convert_username(player_username))
        r = requests.get(endpoint, headers=WarzoneTracker.headers)
        return r.json()

    def get_k_matches(self, k, player_username):
        endpoint = self.matches.format(self._convert_username(player_username))
        r = requests.get(endpoint, headers=WarzoneTracker.headers)
        info = r.json()
        try:
            matches = info['data']['matches']
            n = len(matches)
            next_match = info['data']['metadata']['next']
        except Exception as e:
            if 'errors' in info:
                return info['errors']
            return e
        while k > n:
            endpoint = self.matches_next.format(
                self._convert_username(player_username), next_match)
            r = requests.get(endpoint, headers=WarzoneTracker.headers)
            info = r.json()
            try:
                matches += info['data']['matches']
                n += (len(matches) - n)
                next_match = info['data']['metadata']['next']
            except Exception as e:
                if 'errors' in info:
                    print(info['errors'])
                print(e)
                k = n
                break
        return matches[:k]
    
    def get_matches(self, player_username):
        endpoint = self.matches.format(self._convert_username(player_username))
        r = requests.get(endpoint, headers=WarzoneTracker.headers)
        matches = r.json()
        if 'errors' in matches:
            return matches['errors']
        return matches

    def get_match_info(self, match_id):
        endpoint = self.match_info.format(match_id)
        r = requests.get(endpoint, headers=WarzoneTracker.headers)
        return r.json()
    
    def get_match_stats(self, player_username, match_info):
        base_username = player_username.split('#')[0]
        try:
            _ = match_info['data']['segments'][0]['stats']['kills']['value']
        except:
            return None
        try:
            if not [segment for segment in match_info['data']['segments'] if segment['attributes']['platformUserIdentifier'].lower() != base_username.lower()]:
                return None
        except:
            return None
        
        # TO BE FILLED OUT

        teams = {} # team_fifteen : {'bob':kd, 'mark':kd} and so on
        player_team = {}
        match_id     = match_info['data']['attributes']['id']
        player_count = match_info['data']['metadata']['playerCount']
        mode_name    = match_info['data']['metadata']['modeName']
        timestamp    = match_info['data']['metadata']['timestamp']
        team_count   = match_info['data']['metadata']['teamCount']
        match_kd     = match_info['data']['attributes']['avgKd']['avgKd']
        kd_histogram = match_info['data']['attributes']['kdHistogram']
        link = f'https://cod.tracker.gg/warzone/match/{match_id}?handle={base_username}'
        lifetime_wins = []
        lifetime_games = []
        
        highest_kds = []
        lowest_kds = []
        num_players_private = 0
        for player in match_info['data']['segments']:
            team = player['attributes']['team']
            if team in teams:
                teams[team].append(player)
            else:
                teams[team] = [player]

            curr_username = player['attributes']['platformUserIdentifier']
            if curr_username.lower() == base_username.lower():
                player_team = player['attributes']['team']
                placement = player['metadata']['placement']['value']
            
            if 'lifeTimeStats' in player['attributes']:
                lifetime_wins.append(player['attributes']['lifeTimeStats']['wins'])
                lifetime_games.append(player['attributes']['lifeTimeStats']['gamesPlayed'])
            else:
                num_players_private += 1
        teams_processed = {}
        highest_team_kd = 0
        for team_name, team in teams.items():
            avg = 0
            total = len(team)
            for person in team:
                try:
                    avg += person['attributes']['lifeTimeStats']['kdRatio']
                except Exception:
                    total -= 1
            avg = avg / total
            if avg > highest_team_kd:
                highest_team_kd = avg
            teams_processed[team_name] = avg
        highest_lifetime_kd = []
        for _ in range(3):
            highest_lifetime_kd.append(heapq.heappop(kd_histogram))
        stats = {
            'match_kd': match_kd,
            'lifetime_wins':sum(lifetime_wins)/len(lifetime_wins),
            'lifetime_games':sum(lifetime_games)/len(lifetime_games),
            'highest_team_kd': highest_team_kd,
            'highest_lifetime_kd': highest_lifetime_kd,
            'lowest_lifetime_kd': [0,0,0],
            'team': {
                'kd': 0,
                'placement': 0
            }
        }
        return stats
        
        

    def get_player_kd(self, player_username):
        info = self.get_overview(player_username)
        kd = info['data']['segments'][1]['stats']['kdRatio']['value']
        return kd

    def rank_last_k_lobbies(self, k, player_username):
        matches = self.get_k_matches(k, player_username)
        ids = []
        for match in matches:
            ids.append(match['attributes']['id'])
        kds = []
        for i in ids:
            kds.append((self.get_match_kd(i), i))
        return kds

    def get_match_kd(self, match_id):
        info = self.get_match_info(match_id)
        # entries: (0:lifetime_kd, 1:lifetime_wins, 2:lifetime_games, 3:lifetime_top5, 4:match_kd)
        lifetime_stats = []
        match_kds = []
        highest_kd = 0
        num_players_private = 0
        for player in info['data']['segments']:
            if 'lifeTimeStats' in player['attributes']:
                match_kd = player['stats']['kdRatio']['value']
                lifetime_kd = player['attributes']['lifeTimeStats']['kdRatio']
                wins = player['attributes']['lifeTimeStats']['wins']
                games = player['attributes']['lifeTimeStats']['gamesPlayed']
                top5 = player['attributes']['lifeTimeStats']['top5']
                lifetime_stats.append(
                    (lifetime_kd, wins, games, top5, match_kd))
                highest_kd = lifetime_kd if lifetime_kd > highest_kd else highest_kd
            else:
                num_players_private += 1
                match_kd = player['stats']['kdRatio']['value']
                match_kds.append(match_kd)
        mean_kd = statistics.mean([stat[0] for stat in lifetime_stats])
        median_kd = statistics.median([stat[0] for stat in lifetime_stats])
        match_mean = statistics.mean([stat for stat in match_kds])
        match_median = statistics.median([stat for stat in match_kds])
        return {'median_kd': median_kd, 'mean_kd': mean_kd, 'num_players_private': num_players_private, 'private_players_mean': match_mean, 'private_players_median': match_median}

    def _convert_username(self, username):
        return urllib.parse.quote(username)

if __name__ == '__main__':
    wz = WarzoneTracker()
    username = 'zombieslaya3#1152'
    import json
    with open('./txt/match_info.json') as f:
        info = json.load(f)
    print(wz.get_match_stats(username, info))
    # urllib.parse.unquote('/warzone/profile/atvi/Steezy%234772802/overview')