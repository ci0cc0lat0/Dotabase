# Dotabase
## To use
`pip install -r requirements.txt`

Replace `group_array` with the list if steam32 ids that we wish to collect from.

Replace `data_header` with the columns/feature names you want.
## The what...
This is a script/program that is supposed to be set to run on the hour (give or take 15 minutes). The program collects Dota2 stats from games given `steam32` ids. The data is collected to a giant CSV file. The API used is the opendotaAPI. 
## Purpose
The purpose is to collect a dataset to be used in a data science purpose to give insight that the user wishes, be it Apriori classifications with items, regression analysis among specific features, or inference of how certain factors impact overall-macro gameplay. 
## Functions
- `pretty(dict)` Used to print pretty jason
- `parse_match(matchid)` Used to parse match on call
- `is_on_csv(matchobj)` Used to check if composite key, steam32id and matchid is already saved to CSV
- `get_recentMatch_data(steamid,match_index=0)` Used to get 1 of 20 most recent matches depending on the keywords arguement `match_index` that is defaulted to 0, ie the most recent match. Returns a dict, a so-call `matchobj`, that contains match data, along with steam32id and matchid. When ran in a for-loop, the `match_index` can be incremented to gather other recent matches, eg the second most recent match when `match_index = 1`
- `full_data_dict(matchobj)` Used to get and append additonal data desired from match. Appends to the `matchobj` which will have a steam32id and a matchid to find match data requested. Will most likely parse match, calling `parse_match()`
- `clean_data_dict(matchobj)` used to format the `matchobj` for *only* the data we desire. 
