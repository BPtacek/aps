import api_calls


def request_api(params=None):
    if params is None:
        params = {}
    data = api_calls.make_call('standings', params)
    return data


def data_parser(data):
    parsed_data = {}
    for div_segment in data["records"]:
        for club in div_segment["teamRecords"]:
            tmp = {}
            team, record = club["team"]["name"], club["leagueRecord"]
            division, conference = div_segment["division"]["name"], div_segment["conference"]["name"]
            clinched = "x" if club.get("clinchIndicator", 0) else ""
            standings = {k: v for k, v in list(club.items()) if "Rank" in k}
            goals = {k: v for k, v in list(club.items()) if "goals" in k}

            tmp.update(standings)
            tmp.update(record)
            tmp.update(goals)
            tmp["division"], tmp["conference"], tmp["clinched"] = division, conference, clinched
            parsed_data[team] = tmp

    return(parsed_data)


example = data_parser(request_api())
print(example)