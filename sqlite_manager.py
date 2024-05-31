import sqlite3
DB_FILE_NAME = 'wild_rift.db'


def save_list_to_sqlite(list):
    conn = sqlite3.connect(DB_FILE_NAME)
    cursor = conn.cursor()

    for data in list:
        cursor.execute(
            "INSERT INTO tbl_ranking (time_stamp, date, rank_number, role,hero_img_url,  hero_name, rank_filter ,  win_rate , pick_rate , ban_rate, created_at ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (data['time_stamp'], data['date'], data['rank_number'], data['role'], data['hero_img_url'], data['hero_name'], data['rank_filter'], data['win_rate'], data['pick_rate'], data['ban_rate'], data['created_at']))
    conn.commit()
    conn.close()


def get_latest_time_stamp():
    row = fetch_one(
        '''SELECT time_stamp FROM tbl_ranking ORDER BY time_stamp DESC LIMIT 1''')
    if (row is None):
        return None
    return row[0]


def run_command(command):
    conn = sqlite3.connect(DB_FILE_NAME)
    try:
        cursor = conn.cursor()
        cursor.execute(command)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error executing command: {command}\nError message: {e}")
    finally:
        conn.close()


def fetch_one(command):
    conn = sqlite3.connect(DB_FILE_NAME)
    try:
        cursor = conn.cursor()
        cursor.execute(command)
        row = cursor.fetchone()
        return row
    except sqlite3.Error as e:
        print(f"Error executing command: {command}\nError message: {e}")
    finally:
        conn.close()


def run_migrations():
    migrations_1 = [
        '''CREATE TABLE IF NOT EXISTS tbl_ranking
                      (id INTEGER PRIMARY KEY, time_stamp  integer, date , rank_number integer, role text,hero_img_url text, hero_name text, rank_filter text,  win_rate real, pick_rate real, ban_rate real)''',
        '''ALTER TABLE tbl_ranking ADD COLUMN  created_at TIMESTAMP ''',
        '''CREATE TABLE IF NOT EXISTS tbl_hero
                      (id INTEGER PRIMARY KEY, english  text, chinese text , chinese_translation text, img_url text)''',]
    for command in migrations_1:
        run_command(command)

    hero_count = fetch_one('select count(*) from tbl_hero')
    if (hero_count is None or hero_count[0] == 0):

        try:
            with open('hero.csv', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                champions = lines[1:]
                for champion in champions:
                    conn = sqlite3.connect(DB_FILE_NAME)
                    cursor = conn.cursor()
                    data = champion.split(', ')
                    cursor.execute(
                        "insert into tbl_hero (chinese,chinese_translation,english,img_url) values (?,?,?,?)",
                        (data[0], data[1], data[2], data[3]))
                    conn.commit()
                    conn.close()
                    run_command('', )
        except FileNotFoundError:
            print(f"File not found.")
