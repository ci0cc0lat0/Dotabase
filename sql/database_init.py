import os.path as op

if not op.exists('../.sqliterc.db'):
    sqliterc_file = open("../.sqliterc",'w')
    sqliterc_file.write('.mode COLUMN\n.header ON')
    sqliterc_file.close()


if not op.exists('../dotabase.db'):
    print("it doesnt exist")
    database_file = open("../dotabase.db",'w')
    database_file.close()

    
