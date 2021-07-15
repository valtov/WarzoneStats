import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
FORMAT_ERROR = 'match_info invalid'
MATCH_SUCCESS = 'successfully cached match'
OUTDATED_OVERVIEW = 'overview is older than 10 minutes, need to reset it'
OVERVIEW_NOT_SET = 'overview not set'
TIME_LIMIT = 600
class FirestoreConnection:
    
    def __init__(self):
        cred = credentials.Certificate("./service_account.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def get_users(self):
        docs = self.db.collection('users').stream()
        return [{doc.id:doc.to_dict()} for doc in docs]

    def get_user(self, discord_name):
        doc = self.db.collection('users').document(discord_name).get()
        return doc.to_dict()

    def set_user(self, discord_name, username, platform, default):
        platforms = ['activision', 'playstation', 'xbox', 'battlenet']
        if platform not in platforms:
            return False
        data = {
            platform:username,
            'default':default
        }
        self.db.collection('users').document(discord_name).set(data)
        return True

    def set_matches(self, discord_name, matches):
        matches['timestamp'] = firestore.SERVER_TIMESTAMP
        self.db.collection('matches').document(discord_name).set(matches)
        return True

    def get_matches(self, discord_name):
        doc = self.db.collection('matches').document(discord_name).get()
        matches = doc.to_dict()
        try:
            stamp = matches['timestamp'].timestamp_pb()
            seconds = stamp.ToSeconds()
            curr_seconds = int(time.time())
            print(seconds)
            print(curr_seconds - seconds)
            if curr_seconds - seconds >= TIME_LIMIT:
                return None
            return matches
        except:
            return None

    def set_match_info(self, match_info):
        try:
            id = match_info['data']['attributes']['id']
        except Exception as e:
            return False
        self.db.collection('match_info').document(id).set(match_info)
        return True

    def get_match_info(self, match_id):
        return self.db.collection('match_info').document(match_id).get().to_dict()

    def set_overview(self, discord_name, overview):
        overview['timestamp'] = firestore.SERVER_TIMESTAMP
        self.db.collection('overview').document(discord_name).set(overview)
        return True
    
    def get_overview(self, discord_name):
        doc = self.db.collection('overview').document(discord_name).get()
        overview = doc.to_dict()
        try:
            stamp = overview['timestamp'].timestamp_pb()
            seconds = stamp.ToSeconds()
            curr_seconds = int(time.time())
            print(seconds)
            print(curr_seconds - seconds)
            if curr_seconds - seconds >= TIME_LIMIT:
                return None
            return overview
        except:
            return None

    def test(self, discord_name):
        # new_timestamp = {'timestamp': {'match_info': firestore.SERVER_TIMESTAMP, 'matches':firestore.SERVER_TIMESTAMP}}
        new_timestamp = {'timestamp': firestore.SERVER_TIMESTAMP}
        self.db.collection('overview').document(discord_name).set(new_timestamp, merge=True)
        # doc = self.db.collection('users').document(discord_name).get()
        # curr_timestmap = doc.to_dict()
        # print(new_timestamp)
        # if curr_timestmap is not None and new_timestamp - curr_timestmap >= 600:
        # self.db.collection('users').document(discord_name).set(overview)
        # self.db.collection('users').document(discord_name).set({'timestamp_overview':new_timestamp}})
        # return (True, MATCH_SUCCESS)


if __name__ == '__main__':
    print(f'Started main: {__file__}')
    con = FirestoreConnection()
    con.test('shuttlesneaks#8070')
    # import json

    # with open('./txt/overview.json') as f:
    #     overview = json.load(f)
    
    # fb = con.get_overview('shuttlesneaks#8070')

    # if fb is None:
    #     con.set_overview('shuttlesneaks#8070', overview)
    #     fb = con.get_overview('shuttlesneaks#8070')
    # print(fb)