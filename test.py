from firebase import FirestoreConnection

con = FirestoreConnection()
succ = con.set_user('shuttlesneaks#0000', 'zombieslaa', 'battlenet')
print(succ)
# import requests
# from warzone import WarzoneTracker
# headers = {
#     'authority': 'api.tracker.gg',
#     'cache-control': 'max-age=0',
#     'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
#     'sec-ch-ua-mobile': '?0',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'sec-fetch-site': 'cross-site',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-user': '?1',
#     'sec-fetch-dest': 'document',
#     'accept-language': 'en-US,en;q=0.9',
#     'cookie': '__cfduid=da33e6ee048785828f223ee2a65b3e78d1617577303; X-Mapping-Server=s8; __cflb=02DiuFQAkRrzD1P1mdm8JatZXtAyjoPD2o7G16pDofmnL',
# }

# response = requests.get('https://api.tracker.gg/api/v2/warzone/standard/profile/battlenet/HotteTove%232682/', headers=headers)
# print(response.json()['data'])


# username = 'zombieslaya3#1152'
# obj = WarzoneTracker()

# kds = obj.rank_last_k_lobbies(10, username)
# print(kds)
# with open('stats.txt', 'w') as f:
#     f.write(str(kds))

# print('Done')
