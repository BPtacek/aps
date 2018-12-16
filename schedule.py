import requests, api_calls

#parsing the api call response into two main dicts: dates and games. Dates contains dates, games contains teams, their season record and gameid
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
                score = "{:>} : {:^2}".format(game["teams"]["home"]["score"], game["teams"]["away"]["score"])
            games[date["date"]].setdefault(str(len(games[date["date"]])), (opponents, records, status, gameID, score))

    return dates, games

def display_schedule(data):
    schedule = parse_strings(data)
    for day in range(len(schedule[0])):
        playday = schedule[0][str(day)]
        gamedate = schedule[1][playday]
        print("\n", 70*"=", "\n", "{:^70}".format(playday), "\n", 70*"=", "\n")
        for game in range(1, len(schedule[1][playday])):
            print(gamedate[str(game)][0] + " "*10 + gamedate[str(game)][2] , gamedate[str(game)][1] + " "*19 + gamedate[str(game)][4], sep = "\n")

def fetch_data(params):
    text = api_calls.make_call('schedule', params)
    return text

def collect_inputs():
    inputs = {}
    while input("Wanna input any search parameter? [Y/N]\n\n").lower() == "y":
        input_type = input('What type of parameter? (date [YYYY-MM-DD], startDate [YYYY-MM-DD], endDate [YYYY-MM-DD], teamId)\n\n')
        entry = input('Enter the parameter:\n\n')
        inputs[input_type] = entry
    print(inputs)
    return inputs

def main():
    params = collect_inputs()
    display_schedule(fetch_data(params))

main()
