import modules.helper_functions as hf
import modules.match_processing as mf
import mysql.connector 
import sqlite3 as sql
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    my_con = mysql.connector.connect(
        host="localhost",
        port=3307,
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    my_cur = my_con.cursor()

    games_to_check = 2 # should be 2


    # inital connection
    #con = sql.connect("dotabase.db")
    #cur = con.cursor()

    # get playerids for parsing

    my_cur.execute("SELECT steam_id FROM user;")
    player_ids = my_cur.fetchall()
    player_ids = hf.tuples_to_list(player_ids)

    # check player
    for i in range(0,games_to_check):
        for id in player_ids:
            init_obj = mf.inital_data(id,match_index=i)
            if(hf.is_on_db(cur,init_obj)):
                #print(f"steam_id:{init_obj['steam_id']} and match_id{init_obj['match_id']} are in db")
                continue # if true, skip rest of loop 
            full_obj = mf.get_extra_data(init_obj)
            clean_obj = mf.clean_match_data(full_obj)
            if not clean_obj: continue #I think incase parsing fails from get_extra_data
            
            s_id, m_id = hf.get_ids(clean_obj)
            match_insert = f"INSERT INTO matches(steam_id,match_id) VALUES ({s_id},{m_id})"
            my_cur.execute(match_insert)
            my_con.commit()

            keys, vals = hf.format_insert(clean_obj)
            stat_insert = f"INSERT INTO stat({keys}) VALUES ({vals})"
            my_cur.execute(stat_insert)
            my_con.commit()
            

                    
if __name__ == '__main__':
    main()

