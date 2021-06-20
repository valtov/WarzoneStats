import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
FORMAT_ERROR = 'match_info invalid'
MATCH_SUCCESS = 'successfully cached match'
OUTDATED_OVERVIEW = 'overview is older than 10 minutes, need to reset it'
OVERVIEW_NOT_SET = 'overview not set'
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

    def get_matches(self, discord_name):
        doc = self.db.collection('timestamps').document(discord_name).get()
        timestamps = doc.to_dict()
        try:
            stamp = timestamps['timestamp_matches'].timestamp_pb()
            seconds = stamp.ToSeconds()
            curr_seconds = int(time.time())
            print(seconds)
            print(curr_seconds - seconds)
            if curr_seconds - seconds >= 600:
                return None
            return self.db.collection('matches').document(discord_name).get().to_dict()
        except:
            return None

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
        new_timestamp = {'timestamp_matches': firestore.SERVER_TIMESTAMP}
        self.db.collection('matches').document(discord_name).set(matches)
        self.db.collection('timestamps').document(discord_name).set(new_timestamp, merge=True)
        return True

    def set_match(self, match_info):
        try:
            id = match_info['data']['attributes']['id']
        except Exception as e:
            return False
        self.db.collection('matches').document(id).set(match_info)
        return True

    def set_overview(self, discord_name, overview):
        new_timestamp = {'timestamp_overview': firestore.SERVER_TIMESTAMP}
        # doc = self.db.collection('users').document(discord_name).get()
        # curr_timestmap = doc.to_dict()
        # print(new_timestamp)
        # if curr_timestmap is not None and new_timestamp - curr_timestmap >= 600:
        
        # self.db.collection('users').document(discord_name).set(overview)
        self.db.collection('overview').document(discord_name).set(overview)
        self.db.collection('timestamps').document(discord_name).set(new_timestamp, merge=True)
        return True
    
    def get_overview(self, discord_name):
        doc = self.db.collection('timestamps').document(discord_name).get()
        timestamps = doc.to_dict()
        try:
            stamp = timestamps['timestamp_overview'].timestamp_pb()
            seconds = stamp.ToSeconds()
            curr_seconds = int(time.time())
            print(seconds)
            print(curr_seconds - seconds)
            if curr_seconds - seconds >= 600:
                return None
            return self.db.collection('overview').document(discord_name).get().to_dict()
        except:
            return None

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
    # print(con.get_users())
    # print(con.set_user('shuttlesneaks#8070', 'zombieslaya3#1152', 'activision'))
    # print(con.get_user('shuttlesneaks#8070'))

    import json

    with open('./txt/overview.json') as f:
        overview = json.load(f)
    
    # con.set_overview('shuttlesneaks#8070', overview)

    fb = con.get_overview('shuttlesneaks#8070')

    if fb is None:
        con.set_overview('shuttlesneaks#8070', overview)
        fb = con.get_overview('shuttlesneaks#8070')
    print(fb)