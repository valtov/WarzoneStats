import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class FirestoreConnection:
    
    def __init__(self):
        cred = credentials.Certificate("./service_account.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def get_users(self):
        users_ref = self.db.collection('users').document('discord_mapping')
        docs = users_ref.get()
        return docs.to_dict()

    def get_user(self, discord_name):
        users_ref = self.db.collection('users').document('discord_mapping')
        docs = users_ref.get()
        users = docs.to_dict()
        if discord_name not in users:
            return None
        return users[discord_name]

    def add_user(self, discord_name, platform, username):
        doc_ref = self.db.collection('users').document('discord_mapping')
        doc_ref.set({
            discord_name: {
                'platform':platform,
                'username':username
            }
        }, merge=True)

if __name__ == '__main__':
    print('Started main')
    con = FirestoreConnection()
    print(con.get_users())
    # print(con.get_user('shuttlesneaks#8070'))
    # con.add_user('shuttlesneaks#8070', 'pc', 'zombieslaya3#1152')
    # print(con.get_users())
