import requests
import json

#display the text in the console
def display_schedule(data):
    for date in data["dates"]:
        print("date :", date["date"], "\n")
        for game in date["games"]:
            print(game["teams"]["home"]["team"]["name"], " - ", game["teams"]["away"]["team"]["name"])
            print("{wins}-{losses}-{ot}".format(**game["teams"]["home"]["leagueRecord"]), (len(game["teams"]["home"]["team"]["name"]) - 8 + len(game["teams"]["away"]["team"]["name"]))*" ", "{wins}-{losses}-{ot}".format(**game["teams"]["away"]["leagueRecord"]))





r = requests.get("http://statsapi.web.nhl.com/api/v1/schedule")
text = json.loads(r.text)





display_schedule(text)
input()
