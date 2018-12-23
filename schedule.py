import requests, api_calls
from datetime import date

#parsing the api call response into two main dicts: dates and games. Dates contains dates, games contains teams, their season record, status, gameid, score if game already played/in progress
def parse_strings(data):
    dates = {}
    games = {}
    for date in data["dates"]:
        dates.setdefault(str(len(dates)), date["date"])
        games[date["date"]] = {}
        for game in date["games"]:
            opponents ="{:^24}  -  {:^24}".format(game["teams"]["home"]["team"]["name"], game["teams"]["away"]["team"]["name"])
            records = "{wins:>9}-{losses:0>2}-{ot:0>2}".format(**game["teams"]["home"]["leagueRecord"]) + " " + "{wins:>22}-{losses:0>2}-{ot:0>2}".format(**game["teams"]["away"]["leagueRecord"])
            gameID = game["link"].lstrip('/api/v1/')
            status = game["status"]["detailedState"]
            if status != "Scheduled":
                score = "{:>} : {:<2}".format(game["teams"]["home"]["score"], game["teams"]["away"]["score"])
                basic_game_data = api_calls.make_call(game["link"].lstrip("/api/v1/"), {})
                czechs = [" - ".join([basic_game_data["gameData"]["players"][player]["fullName"], basic_game_data["gameData"]["players"][player]["currentTeam"]["triCode"]]) for player in basic_game_data["gameData"]["players"] if basic_game_data["gameData"]["players"][player]["nationality"] == "CZE"]
            else:
                score = "- : -"
                czechs = ["Czech players not confirmed yet"]
            if czechs:
                czechs = ", ".join(czechs)
            else:
                czechs = "no czechs"
            games[date["date"]].setdefault(str(len(games[date["date"]])), {"opponents" : opponents, "records" : records, "status" : status, "gameID" : gameID, "score" : score, "czechs" : czechs})

    return dates, games

#function tht prints out to the stdout collected and parsed search results
def display_schedule(data):
    schedule = parse_strings(data)
    for day in range(len(schedule[0])):
        playday = schedule[0][str(day)]
        gamedate = schedule[1][playday]
        print("\n", 84*"=", "\n", "{:^70}".format(playday), "\n", 84*"=", "\n")
        for game in range(len(gamedate)):
            print(gamedate[str(game)]["opponents"] + " "*10 + gamedate[str(game)]["status"] , gamedate[str(game)]["records"] + " "*19 + gamedate[str(game)]["score"], "{:^51}".format(gamedate[str(game)]["czechs"]), sep = "\n")

#function to run the api call and collecting the result
def fetch_data(params):
    text = api_calls.make_call('schedule', params)
    return text

#function handling the user inputs if user wishes to provide parameters of the search
def collect_inputs():
    inputs = {}
    while input("Wanna input any search parameter? [Y/N]\n\n").lower() == "y":
        input_type = input('What type of parameter? (date [YYYY-MM-DD], startDate [YYYY-MM-DD], endDate [YYYY-MM-DD], teamId)\n\n')
        entry = input('Enter the parameter:\n\n')
        inputs[input_type] = entry
    if inputs:
        return inputs
    else:
        return {"date" : str(date.today())}

#main function running the whole thing
def main():
    params = collect_inputs()
    display_schedule(fetch_data(params))

if __name__ == "__main__":
    main()
    input()
