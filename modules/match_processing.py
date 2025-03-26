import requests
import time

def inital_data(steam_id,match_index = 0):
    '''Gets the recent data, importantly the match_id. Returns an object'''
    response = requests.get(f'https://api.opendota.com/api/players/{steam_id}/matches')
    time.sleep(1)
    data = response.json()
    print(f"Game {match_index} for steamID: {steam_id}, for matchID: {data[match_index]['match_id']}")
    data[match_index]["steam_id"] = steam_id
    return data[match_index]

def get_extra_data(match_obj):
    ''' Gets extra (parse needed) data from another request 
    appends the data to the passing object'''
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
            
            # this data must match the object data below
            apm = data['players'][player_index]["actions_per_min"]
            time_spent_dead = data['players'][player_index]["life_state_dead"]
            lane = data['players'][player_index]["lane"]
            lane_role = data['players'][player_index]["lane_role"]
            xpm = data['players'][player_index]["xp_per_min"]
            gpm = data['players'][player_index]["gold_per_min"]
            hero_damage = data['players'][player_index]["hero_damage"]
            hero_healing = data['players'][player_index]["hero_healing"]
            last_hits = data['players'][player_index]["last_hits"]
            hero_healing = data['players'][player_index]["hero_healing"]
            
            # thid data must match the res data above
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
    '''Strips the match_obj of undesired data.
    Returns a data object that reflects final form of data'''
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

    # this order has to match the database? or does it keyword
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
    '''Parses the specific match from opendota with given match_id'''
    parse_url = f'https://api.opendota.com/api/request/{match_id}'
    requests.post(parse_url)
    time.sleep(20)

