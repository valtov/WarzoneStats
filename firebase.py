import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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

if __name__ == '__main__':
    print('Started main')
    con = FirestoreConnection()
    print(con.get_users())
    print(con.set_user('shuttlesneaks#8070', 'zombieslaya3#1152', 'activision'))
    print(con.get_user('shuttlesneaks#8070'))
