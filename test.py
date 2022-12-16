import requests
import json

match_index = 0
working_matchID = 6914252885
# 6914252885 6914307843 1 0
ant_recentMatch= f"https://api.opendota.com/api/players/118728071/recentMatches"
response = requests.get(ant_recentMatch)
data = response.json()
pretty_data = json.dumps(data[0], indent = 2)
#print(pretty_data)




# Recent matches api
match_id = data[match_index]['match_id']
player_slot = data[match_index]['player_slot']
kills = data[match_index]['kills']
deaths = data[match_index]['deaths']
assists = data[match_index]['assists']
xpm = data[match_index]['xp_per_min']
gpm = data[match_index]['gold_per_min'] # diff
hero_id = data[match_index]['hero_id']
duration = data[match_index]['duration']
last_hits = data[match_index]['last_hits']
lane = data[match_index]['lane']
lane_role = data[match_index]['lane_role']
start_time = data[match_index]['start_time']
hero_damage = data[match_index]['hero_damage']
hero_healing = data[match_index]['hero_healing']
#apm = data[0]['match_id']
#win = data[0]['match_id']
#patch = data[0]['match_id'] # diff
#side = data[0]['match_id']
#tower_damage = data[0]['match_id']

test_slot = player_slot if player_slot < 5 else player_slot-123
print(test_slot)
print(player_slot)

### PARSING
parse_url = f'https://api.opendota.com/api/request/6912423974'
parse_request = requests.post(parse_url)
parse_request_json = parse_request.json()
parse_job_id = parse_request_json['job']['jobId']
#job_id = parse_request['job']['jobId']
print(parse_job_id)
parse_job = f'https://api.opendota.com/api/request/{parse_job_id}'
print(parse_job)

### matches api
ant_matchData =  f'https://api.opendota.com/api/matches/{working_matchID}'
response_match =requests.get(ant_matchData)
data_match = response_match.json()
pretty_data_match = json.dumps(data_match, indent = 2)
#print(pretty_data_match)
#print(data_match)
apm = data_match['players'][test_slot]["actions_per_min"]
time_spent_dead = data_match['players'][test_slot]["life_state_dead"]
#patch = data_match['players'][test_slot]["patch"]

#print(data_match['players'][player_slot]['player_slot'])
print(apm, time_spent_dead)