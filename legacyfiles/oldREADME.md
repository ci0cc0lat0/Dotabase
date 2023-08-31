# Dotabase
## Use and functionality `gather-script.py`
This code is ran by manual use in a CLI environment. Typically the `playerid` list in main would be very low if not one ( as to not go over the APIs limits) and would appended the the same CSV that `main.py` uses

## Use and functionality `main.py`
This program is designed to take a set of steam32 ids and report back specific stats from Dota 2 matches those players are in. 
The stats are pulled from Opendota API and are called per player, per match on a set interval to gather all possible matches.

The code can be adapted easily by changing the `group_array` to the steam_ids that are desired, and the `range()` amount for the for-loop  in the main function.

**Idealy**: 
- code would run every 30 to 45 minutes from a cron job ( to catch even quick games )
- the code will not record a match ID or Steam ID pair that is already in the csv
- `group_array` would have a atleast a single steam32 ID in it
- `range()` would be set to 2 ( this is to catch any errors on the API's side, or quick games)
- different stats could be collected if knowledge of the Opendota API is known

## Description of functions
- `pretty()` used to print out pretty json during debugging
- `get_recent_match()` used to get the most recent match_ids from the specific steam_id given
- `get_unrecorded_match()` used to return game data of the match and steam ID pairs not in csv
- `get_recent_match_data()` used to return a dict of data from the "recentMatch" API call
- `get_match_data()` used to return the extra data wanted not found int he "recentMatch" API call
- `parse_match()` A helped function used in `get_match_data()` to parse a game if it needs parsing as that "extra data" is hidden behind an Opendota API parse

## The Flow of data
### Stage 0: Code write up
The steps for acccessing the api and recording data is done.

### Stage 1: Parsing and data collecting
This will be done through cronjobs every half hour with the set of steam32 ids provided in the code.
This will take a while as I require a numerous amount of game data to work with.

### Stage 2: Data scrubbing and analytics
Here, The data will be analyized and ran through jupyter. Visualizations and stats will be shown and collected.

### Stage 3: Repeat stages 1 and 2
