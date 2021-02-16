from configparser import ConfigParser
import mysql.connector
import time

#Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")
production_db = config_object["PRODUCTIONDB"]
local_db = config_object["LOCALDB"]

# connect with production DB
production_db_con = mysql.connector.connect(user = production_db["user"],password = production_db["password"],host = production_db["host"],database = production_db["database"])
production_db_cursor = production_db_con.cursor()

query = production_db_cursor.execute("Select count(*) from Dictionary")
total_rows = production_db_cursor.fetchone()[0]

if total_rows > 0:
    limit = 1000
    mod = total_rows % limit
    if mod > 0:
        loop_count = (total_rows // limit) + 1
    else:
        loop_count = (total_rows // limit)

    # connect with local DB
    local_db_con = mysql.connector.connect(user = local_db["user"],password = local_db["password"],host = local_db["host"],database = local_db["database"])
    local_db_cursor = local_db_con.cursor()
    
    for i in range(loop_count):
        offset = i * limit
        query_limited_data = production_db_cursor.execute("Select * from Dictionary Limit %(offset)s, %(limit)s",{'offset' : offset, 'limit' : limit})
        data = production_db_cursor.fetchall()
        
        stmt = "INSERT INTO dictionary (word, explanation) VALUES (%s, %s)"
        local_db_cursor.executemany(stmt, data)
        local_db_con.commit()
        
        time.sleep(1)

    local_db_con.close()
else:
    print("This table is empty.")

production_db_con.close()