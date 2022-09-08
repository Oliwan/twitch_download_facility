import requests

print("Trying to get the key")
client_id = 'INSERT_CLIENT_ID'
client_secret = 'INSERT_CLIENT_SECRET'

body = {
    'client_id': client_id,
    'client_secret': client_secret,
    "grant_type": 'client_credentials'
}
r = requests.post('https://id.twitch.tv/oauth2/token', body)

#data output
keys = r.json();

headers = {
    'Client-ID': client_id,
    'Authorization': 'Bearer ' + keys['access_token']
}

print("Access token is:",keys["access_token"])
print("Looking for the top-100 games")

num_top_games = '100'
stream = requests.get('https://api.twitch.tv/helix/games/top?first='+ num_top_games, headers=headers)

game_data = stream.json()

ids = []
game_names = []

for game in game_data["data"]:
    ids.append(game['id'])
    game_names.append(game['name'])

print("Top-100 games taken successfully")
print("Now getting user info")

data = []
num_utenti = []


for i in range(len(ids)):
    stream = requests.get('https://api.twitch.tv/helix/streams?game_id='+ids[i] + '&first=100', headers=headers)
    stream_data = stream.json()        
    data.append(stream_data["data"])
    num_utenti.append(len(stream_data["data"]))

print("user info taken successfully")
print("Building the data model")

from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

import pandas as pd

list_of_dataframes = []

#converting into dataframe
for d in data:
    single_game_df = pd.DataFrame.from_dict(d)
    list_of_dataframes.append(single_game_df)
name_file = str(timestamp)
df = pd.concat(list_of_dataframes)

print("data model built, saving to csv")
df.to_csv(name_file+".csv")
print("done.")
