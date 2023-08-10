import requests
import json
import time
import csv
import pandas as pd



### Utility, QOL functions for testing purposes
# input is a json object, returns readable json
def pretty(json_object, indent = 4):
    return json.dumps(json_object, indent = indent)

### Workhorse functions
# input an array of ids, returns the match object with steamid appended
def get_recent_match(steamid_array, match_index = 0):
    
    if not isinstance(steamid_array, list):
        steamid_array = [steamid_array]

    recent_match_array = []
    for steam_id in steamid_array:
        response = requests.get(f"https://api.opendota.com/api/players/{steam_id}/recentMatches")
        time.sleep(1)
        data = response.json()
        print(f"Game {match_index} for steamID: {steam_id}")
        data[match_index]["steam_id"] = steam_id
        recent_match_array.append(data[match_index])
    return recent_match_array 

# input single match, returns data object we want
def get_recent_match_data(match_objects):
    if not isinstance(match_objects, list):
        match_objects = [match_objects]

    data_object_array = []
    for each_object in match_objects:
        steam_id = each_object['steam_id']
        match_id = each_object['match_id']
        player_slot = each_object['player_slot']
        kills = each_object['kills']
        deaths = each_object['deaths']
        assists = each_object['assists']
        xpm = each_object['xp_per_min']
        gpm = each_object['gold_per_min'] 
        hero_id = each_object['hero_id']
        duration = each_object['duration']
        last_hits = each_object['last_hits']
        lane = each_object['lane']
        lane_role = each_object['lane_role']
        start_time = each_object['start_time']
        hero_damage = each_object['hero_damage']
        hero_healing = each_object['hero_healing']

        data_object = {
        "steam_id":steam_id,
        "match_id":match_id,
        "player_slot":player_slot,
        "kills":kills,
        "deaths":deaths,
        "assists":assists,
        'xpm':xpm,
        'gpm':gpm,
        'hero_id':hero_id,
        'duration':duration,
        'last_hits':last_hits,
        'lane':lane,
        'lane_role':lane_role,
        'start_time':start_time,
        'hero_damage':hero_damage,
        'hero_healing':hero_healing
        }
        
        data_object_array.append(data_object)
    return data_object_array

# this data requires a parse, adds the extra info we cant get from recentMatch api
def get_match_data(data_objects):
    if not isinstance(data_objects, list):
        data_objects = [data_objects]
    
    data_obj_appended = []
    for each_object in data_objects:
        while True:
            match_id = each_object['match_id']
            obj_player_slot = each_object['player_slot']
            player_index = obj_player_slot if obj_player_slot < 5 else obj_player_slot-123
            try:
                response = requests.get(f'https://api.opendota.com/api/matches/{match_id}')
                
                data = response.json()

                game_mode = data['game_mode']
                if(game_mode != 22 | game_mode != 16 | game_mode != 4):
                    break

                apm = data['players'][player_index]["actions_per_min"]
                time_spent_dead = data['players'][player_index]["life_state_dead"]
                lane = data['players'][player_index]["lane"]
                lane_role = data['players'][player_index]["lane_role"]


                each_object['apm'] = apm
                each_object["time_spent_dead"] = time_spent_dead
                each_object["lane_role"] = lane_role
                each_object["lane"] = lane
                
                data_obj_appended.append(each_object) # trying ot get here
            except Exception as e:
                parse_match(match_id)
            else:
                break
    return data_obj_appended

def parse_match(match_id):
    parse_url = f'https://api.opendota.com/api/request/{match_id}'
    requests.post(parse_url)
    #parse_request = requests.post(parse_url)
    #parse_request_json = parse_request.json()
    #parse_job_id = parse_request_json['job']['jobId']
    time.sleep(20)

def get_unrecorded_matches(match_object_array):
    unadded_match_objects = []
    for match_object in match_object_array:
        steamid = match_object['steam_id']
        matchid = match_object['match_id']
        df = pd.read_csv('dota.csv')
        df = df[['steam_id', 'match_id']]
        checked_table = df[(df['steam_id'] == steamid) & (df['match_id'] == matchid)]
        if (checked_table.size == 0): # meaning that match and steam id arent recorded yet
            unadded_match_objects.append(match_object)
    return unadded_match_objects
            
def main():
    # ant gub json andy matt rawb josh milo
    group_array = [118728071,112127522,122334023,106975318,110352369,171149001,380821421,133355068]

    data_header = [
    'steam_id','match_id','player_slot','kills',
    'deaths','assists','xpm','gpm','hero_id',
    'duration','last_hits','lane','lane_role',
    'start_time','hero_damage','hero_healing','apm','time_spent_dead']
    for i in range(2):
    
        with open('dota.csv', 'a') as file:
            writer = csv.DictWriter(file, fieldnames=data_header)
            if file.tell() == 0:
                writer.writeheader()
            
        match_object_array = get_recent_match(group_array,i)
        unrecorded_match_objects = get_unrecorded_matches(match_object_array)
        sorted_data = get_recent_match_data(unrecorded_match_objects) # this function can probably be at the end, as to sort fully after all is appeneded
        full_data = get_match_data(sorted_data)
        #print(pretty(full_data))
        
        with open('dota.csv', 'a') as file:
            writer = csv.DictWriter(file, fieldnames=data_header)
            writer.writerows(full_data)
            file.close()

    

if __name__ == '__main__':
    main()
    