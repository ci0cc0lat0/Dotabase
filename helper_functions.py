import json
import pandas as pd
import sqlite3

def pretty(json_object: dict, indent: int = 4) -> None:
    '''Used to print out json objects as to read/debug them'''
    print(json.dumps(json_object, indent = indent))

def is_on_csv(match_obj: dict):
        ''' Legacy function that would check a CSV if the steam and match id (composite key) were in the csv'''
        steamid = match_obj['steam_id']
        matchid = match_obj['match_id']
        df = pd.read_csv('dota.csv')
        df = df[['steam_id', 'match_id']]
        checked_table = df[(df['steam_id'] == steamid) & (df['match_id'] == matchid)]

        # if empty table, no matching steam+match id
        if (checked_table.size == 0): return False
        else: return True

def is_on_db(cur: sqlite3.Cursor,match_obj: dict) -> bool:
    '''Checks the match table against the given steam and match id. A return of False means the query length yeilded 0 meaning its not on the db yet.'''
    res = cur.execute(f"SELECT * FROM match WHERE steam_id={match_obj['steam_id']} AND match_id={match_obj['match_id']}")
    res = res.fetchall()
    if(len(res) == 0):
         return False
    else:
         return True

def tuples_to_list(tuple_list:list) -> list:
    if(type(tuple_list) == tuple):
         return [tuple_list[0]]
    '''Meant for taking a single or first tuple of the list'''
    return_list = []
    for item in tuple_list:
        return_list.append(item[0])
    return return_list

def format_insert(final_obj):
     keys = list(final_obj.keys())
     vals = list(final_obj.values())
     
     # turn list[any] into list[str] so I can join()
     val_list = []
     for item in vals:
          val_list.append(str(item))

     keys = ', '.join(keys)
     vals = ', '.join(val_list)
     return (keys, vals)
    
def get_ids(final_obj):
     steam_id = final_obj["steam_id"]
     match_id = final_obj["match_id"]
     return str(steam_id), str(match_id)