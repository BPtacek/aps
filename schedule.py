import requests, api_calls

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
            else:
                score = "- : -"
            games[date["date"]].setdefault(str(len(games[date["date"]])), (opponents, records, status, gameID, score))

    return dates, games

#function tht prints out to the stdout collected and parsed search results
def display_schedule(data):
    schedule = parse_strings(data)
    for day in range(len(schedule[0])):
        playday = schedule[0][str(day)]
        gamedate = schedule[1][playday]
        print("\n", 73*"=", "\n", "{:^70}".format(playday), "\n", 73*"=", "\n")
        for game in range(len(schedule[1][playday])):
            print(gamedate[str(game)][0] + " "*10 + gamedate[str(game)][2] , gamedate[str(game)][1] + " "*19 + gamedate[str(game)][4], sep = "\n")

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
            print(inputs)
    return inputs

#main function running the whole thing
def main():
    params = collect_inputs()
    display_schedule(fetch_data(params))

if __name__ == "__main__":
    main()
