import helper_functions as hf
import match_processing as mf
import sqlite3 as sql
import time

def main():
    games_to_check = 40 # should be 2


    # inital connection
    con = sql.connect("dotabase.db")
    cur = con.cursor()

    # get playerids for parsing
    res = cur.execute("SELECT steam_id FROM user")
    player_ids = res.fetchall()
    player_ids = hf.tuples_to_list(player_ids)

    # check player
    for i in range(0,games_to_check):
        for id in player_ids:
            init_obj = mf.inital_data(id,match_index=i)
            if(hf.is_on_db(cur,init_obj)): continue # if true, skip rest of loop 
            full_obj = mf.get_extra_data(init_obj)
            clean_obj = mf.clean_match_data(full_obj)
            if not clean_obj: continue #I think incase parsing fails from get_extra_data
            
            s_id, m_id = hf.get_ids(clean_obj)
            match_insert = f"INSERT INTO match(steam_id,match_id) VALUES ({s_id},{m_id})"
            cur.execute(match_insert)
            con.commit()

            keys, vals = hf.format_insert(clean_obj)
            stat_insert = f"INSERT INTO stat({keys}) VALUES ({vals})"
            cur.execute(stat_insert)
            con.commit()
        sleep_time = 30
        print(f"I sleep for {sleep_time}")
        time.sleep(sleep_time)
            

                    
if __name__ == '__main__':
    main()

