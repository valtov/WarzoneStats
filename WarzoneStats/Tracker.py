from WarzoneTracker.Api import Api
from WarzoneTracker.Parser import Parser

class Tracker:

    def __init__(self, username):
        self.api = Api()
        self.parser = Parser()
        self.username = username
        #url_username = api._convert_username(username)
    
    def test(self):
        print("Test", __name__, self.username)
        
    def get_kd(self):
        #url_username = self.api._convert_username(username)
        overview = self.api.get_overview(self.username)
        kd = self.parser.get_player_kd(overview)
        return kd

    def average_last_k_matches(self, k=10):
        matches = self.api.get_k_matches(k, self.username)
        return matches

if __name__ == '__main__':
    username = 'zombieslaya3#1152'
    tracker = Tracker(username)
    tracker.test()
    kd = tracker.get_kd()
    print('KD =', kd)
    k_matches = tracker.average_last_k_matches()
    print(k_matches)

   
