from datetime import datetime, date, timedelta
import psycopg2
from psycopg2 import sql
import re

start_time = datetime.now()
print(start_time)

# Database connection parameters
host = 'localhost'
port = '5432'
database = 'MOEX'
user = 'postgres'
password = 'postgres'

# Create a connection to the database
conn = psycopg2.connect(
    host=host,
    port=port,
    dbname=database,
    user=user,
    password=password
)

# Create a cursor object using the connection
cur = conn.cursor()
cur_insert = conn.cursor()

channels_select_statement = """
select c.id,
       c.channel_name,
       c.channel_db_table,
       coalesce(scmm.date_to, '2021-01-01') date_to
from tg_channels.channels c
    left join
    (
        select channel_id,
               max(date_to) date_to
        from log.stock_channel_messages_matching
        group by channel_id
    ) scmm
        on c.id = scmm.channel_id
order by c.id
"""

aliases_select_statement = """
select secid,
       search_string,
       is_strong
from moex_stocks.stock_search_aliases ssa
order by secid asc,
         is_strong desc
"""

insert_matches_statement = """
    INSERT INTO integration.list_of_matches (secid, message_id, channel_db_table, search_string, is_strong, matching_string, message, date_published) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""

insert_log_statement = """
    INSERT INTO log.stock_channel_messages_matching (channel_id, date_from, date_to, message_count, matches_count) 
    VALUES (%s, %s, %s, %s, %s);
"""

cur.execute(channels_select_statement)    
rows = cur.fetchall()
cur.execute(aliases_select_statement)
aliases = cur.fetchall()

for row in rows:
    channel_id = row[0]
    channel_name = row[1]
    channel_db_table = row[2]
    date_from = row[3]
    
    #ТУТ НУЖНО БУДЕТ ПОЛУЧИТЬ ИЗ ТАБЛИЦЫ С ЛОГАМИ ДАТУ, С КОТОРОЙ НАЧИНАЕМ АНАЛИЗ
    #date_from = datetime.strptime('2021-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    date_to = date_from
    select_messages_statement = f"""
    select message_id, message, date_published 
    from tg_channels.{channel_db_table} 
    where date_published > %s and message is not null
    order by date_published asc
    """
    cur.execute(select_messages_statement, (date_from,))
    messages = cur.fetchmany(1000)
    message_count = 0
    matches_count = 0
    matched_substring = ''
    while (messages):
        for message in messages:
            for aliase in aliases:
                escaped_included_string = re.escape(aliase[1])
                pattern = (
                r'(?<![a-zA-Zа-яА-Я0-9])'  
                r'[\s#()\[\]"\']*'          
                + escaped_included_string  
                + r'[\s#()\[\]"\']*'       
                r'(?![a-zA-Zа-яА-Я0-9])'   
                )
                message_string = message[1]
                match = re.search(pattern, message_string) 
                if match:
                    start, end = match.start(), match.end()
                    start = max(start - 1, 0)
                    end = min(end + 1, len(message_string))
        
                    matched_substring = message_string[start:end]
                    cur_insert.execute(insert_matches_statement, (aliase[0], message[0],channel_db_table,aliase[1],aliase[2],matched_substring, message_string, message[2]))
                    conn.commit()
                    matches_count = matches_count + 1
            date_to = message[2]
            message_count = message_count + 1
            if message_count%10000 == 0:
                print(message_count)
        messages = cur.fetchmany(1000)
    cur.execute(insert_log_statement, (channel_id, date_from,date_to,message_count, matches_count))
    conn.commit()
    print(channel_name)
cur.close()
conn.close()    

finish_time = datetime.now()
print(finish_time)
print(finish_time-start_time)