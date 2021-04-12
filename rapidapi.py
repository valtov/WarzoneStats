import requests

#url = "https://call-of-duty-modern-warfare.p.rapidapi.com/warzone-matches/{}/{}"

url = "https://call-of-duty-modern-warfare.p.rapidapi.com/warzone-matches/Amartin743/psn"


headers = {
    'x-rapidapi-key': "64ce7ce5ccmsh7621c0234bdc362p19ef8ejsn61e486dcca41",
    'x-rapidapi-host': "call-of-duty-modern-warfare.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)