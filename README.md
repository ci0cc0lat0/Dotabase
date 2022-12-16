# Dotabase
## Use and functionality
This program is designed to take a set of steam32 ids and report back specific stats from Dota 2 matches those players are in. 
The stats are pulled from Opendota API and are called per player, per match on a set interval to gather all possible matches.

The code can be adapted easily by changing the `group_array` to the steam_ids that are desired, and the `range()` amount for the for-loop  in the main function.
Idealy: 
- the code will not record duplicates already in the csv
- `group_array` would have a atleast a single steam32 ID in it
- `range()` would be set to 2 ( this is to catch any errors on the API's side)
- code would run every 30 to 45 minutes from a cron job ( to catch even quick games )
- different stats could be collected if knowledge of the Opendota API is known

## The Flow of data
### Stage 0: Code write up
The steps for acccessing the api and recording data is done.

### Stage 1: Parsing and data collecting
This will be done through cronjobs every half hour with the set of steam32 ids provided in the code.
This will take a while as I require a numerous amount of game data to work with.

### Stage 2: Data scrubbing and analytics
Here, The data will be analyized and ran through jupyter. Visualizations and stats will be shown and collected.

### Stage 3: Repeat stages 1 and 2
