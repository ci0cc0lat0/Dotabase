import requests
import json
import time
import csv
import pandas as pd

def pretty(json_object, indent = 4):
    print(json.dumps(json_object, indent = indent))

def inital_data(steam_id,match_index = 0):
    response = requests.get(f'https://api.opendota.com/api/players/{steam_id}/matches')
    time.sleep(1)
    data = response.json()
    print(f"Game {match_index} for steamID: {steam_id}, for matchID: {data[match_index]['match_id']}")
    data[match_index]["steam_id"] = steam_id
    return data[match_index]

def get_extra_data(match_obj):
    match_id = match_obj['match_id']
    player_slot = match_obj['player_slot']
    player_index = player_slot if player_slot < 5 else player_slot-123
    parse_counter = 0
    while True:
        try:
            response = requests.get(f'https://api.opendota.com/api/matches/{match_id}')
            data = response.json()
            game_mode = data['game_mode']
            if(game_mode != 22 | game_mode != 16 | game_mode != 4):
                match_obj = {}
                break
            
            apm = data['players'][player_index]["actions_per_min"]
            time_spent_dead = data['players'][player_index]["life_state_dead"]
            lane = data['players'][player_index]["lane"]
            lane_role = data['players'][player_index]["lane_role"]
            xpm = data['players'][player_index]["xp_per_min"]
            gpm = data['players'][player_index]["gold_per_min"]
            hero_damage = data['players'][player_index]["hero_damage"]
            hero_healing = data['players'][player_index]["hero_healing"]
            last_hits = data['players'][player_index]["last_hits"]
            hero_damage = data['players'][player_index]["hero_damage"]
            hero_healing = data['players'][player_index]["hero_healing"]
            
            
            match_obj['apm'] = apm
            match_obj["time_spent_dead"] = time_spent_dead
            match_obj["lane_role"] = lane_role
            match_obj["lane"] = lane
            match_obj['hero_damage'] = hero_damage
            match_obj['hero_healing'] = hero_healing
            match_obj['last_hits'] = last_hits
            match_obj['xp_per_min'] = xpm
            match_obj['gold_per_min'] = gpm

        except Exception as e:
            if parse_counter > 2:
                match_obj = {}
                break
            parse_match(match_id)
            print("parse counter",parse_counter)
            parse_counter += 1
            
        else:
            break
    return match_obj

def clean_match_data(match_obj):
    if not (match_obj): return match_obj

    steam_id = match_obj['steam_id']
    match_id = match_obj['match_id']
    player_slot = match_obj['player_slot']
    kills = match_obj['kills']
    deaths = match_obj['deaths']
    assists = match_obj['assists']
    xpm = match_obj['xp_per_min']
    gpm = match_obj['gold_per_min'] 
    hero_id = match_obj['hero_id']
    duration = match_obj['duration']
    last_hits = match_obj['last_hits']
    lane = match_obj['lane']
    lane_role = match_obj['lane_role']
    start_time = match_obj['start_time']
    hero_damage = match_obj['hero_damage']
    hero_healing = match_obj['hero_healing']
    apm = match_obj['apm']
    time_spent_dead = match_obj['time_spent_dead']

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
        'hero_healing':hero_healing,
        'apm':apm,
        'time_spent_dead': time_spent_dead
        }
    return data_object

def parse_match(match_id):
    parse_url = f'https://api.opendota.com/api/request/{match_id}'
    requests.post(parse_url)
    time.sleep(20)

def is_on_csv(match_obj):
        steamid = match_obj['steam_id']
        matchid = match_obj['match_id']
        df = pd.read_csv('dota.csv')
        df = df[['steam_id', 'match_id']]
        checked_table = df[(df['steam_id'] == steamid) & (df['match_id'] == matchid)]

        # if empty table, no matching steam+match id
        if (checked_table.size == 0): return False
        else: return True

def main():
    playerid = [110352369]
    data_header = [
    'steam_id','match_id','player_slot','kills',
    'deaths','assists','xpm','gpm','hero_id',
    'duration','last_hits','lane','lane_role',
    'start_time','hero_damage','hero_healing','apm','time_spent_dead']
    games_to_check = 80

    for i in range(games_to_check):
        for id in playerid:
            inital_obj = inital_data(id,match_index=i)
            if is_on_csv(inital_obj):
                # if obj is already in csv, skip rest of forloop
                continue
            full_obj = get_extra_data(inital_obj)
            clean_obj = clean_match_data(full_obj)
            if not clean_obj: continue

            with open('dota.csv', 'a', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=data_header)
                    writer.writerows([clean_obj])
                    file.close()

if __name__ == '__main__':
    main()
