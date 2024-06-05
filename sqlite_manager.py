import sqlite3
DB_FILE_NAME = 'wild_rift.db'


def save_new_champs(champs):
    if champs is None:
        return
    champs = list(set(champs))
    conn = sqlite3.connect(DB_FILE_NAME)
    cursor = conn.cursor()

    for data in champs:
        cursor.execute(
            "INSERT INTO tbl (chinese, img_url) VALUES (?, ?)",
            (data['chinese'], data['img_url']))
        data['id'] = cursor.lastrowid
    conn.commit()
    conn.close()


def save_list_to_sqlite(list):
    conn = sqlite3.connect(DB_FILE_NAME)
    cursor = conn.cursor()

    for data in list:
        cursor.execute(
            "INSERT INTO tbl_rank (time_stamp, date, rank_number, role,champ_id, rank_filter ,  win_rate , pick_rate , ban_rate ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (data['time_stamp'], data['date'], data['rank_number'], data['role'], data['champ_id'], data['rank_filter'], data['win_rate'], data['pick_rate'], data['ban_rate'], ))
    conn.commit()
    conn.close()


def get_latest_time_stamp():
    row = fetch_one(
        '''SELECT time_stamp FROM tbl_rank ORDER BY time_stamp DESC LIMIT 1''')
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


def fetch_all(command):
    conn = sqlite3.connect(DB_FILE_NAME)
    try:
        cursor = conn.cursor()
        cursor.execute(command)
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Error executing command: {command}\nError message: {e}")
    finally:
        conn.close()


def run_migrations():
    migrations = [
        '''CREATE TABLE IF NOT EXISTS tbl_rank
                      (id INTEGER PRIMARY KEY, time_stamp  integer, date , rank_number integer, role text,hero_img_url text, hero_name text, rank_filter text,  win_rate real, pick_rate real, ban_rate real)''',
        '''ALTER TABLE tbl_rank ADD COLUMN  created_at TIMESTAMP ''',
        '''CREATE TABLE IF NOT EXISTS tbl_hero
                      (id INTEGER PRIMARY KEY, english  text, chinese text , chinese_translation text, img_url text)''',
    ]
    for command in migrations:
        run_command(command)

    insert_champion()


def insert_champion():
    champ_count = fetch_one('select count(*) from tbl_champion')
    if (champ_count is None or champ_count[0] == 0):
        try:
            with open('champ.csv', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                champions = lines[1:]
                for champion in champions:
                    conn = sqlite3.connect(DB_FILE_NAME)
                    cursor = conn.cursor()
                    data = champion.split(', ')
                    cursor.execute(
                        "insert into tbl_champion (chinese,chinese_translation,english,img_url) values (?,?,?,?)",
                        (data[0], data[1], data[2], data[3]))
                    conn.commit()
                    conn.close()
                    run_command('', )
        except FileNotFoundError:
            print(f"File not found.")


def add_hero_id_to_ranking():
    hero_id_exist = fetch_one(
        "SELECT COUNT(*) AS CNTREC FROM pragma_table_info('tbl_rank') WHERE name='hero_id' ")
    if (hero_id_exist is None or hero_id_exist[0] == 0):
        run_command('''ALTER TABLE tbl_rank ADD COLUMN  hero_id INTEGER ''')
        heroes = fetch_all('select id, chinese from tbl_hero')
        try:
            with open('hero.csv', 'r', encoding='utf-8') as file:

                heroes = heroes
                for hero in heroes:
                    conn = sqlite3.connect(DB_FILE_NAME)
                    cursor = conn.cursor()
                    data = hero.split(', ')
    #                 UPDATE software SET software.purchprice =
    #  (SELECT purchprice FROM softwerecost WHERE software.id = softwerecost.id)
    #  WHERE id IN (SELECT id FROM softwarecost);
                    cursor.execute(
                        "insert into tbl_hero (chinese,chinese_translation,english,img_url) values (?,?,?,?)",
                        (data[0], data[1], data[2], data[3]))
                    conn.commit()
                    conn.close()
                    run_command('', )
        except FileNotFoundError:
            print(f"File not found.")


def set_db():
    migrations = [
        '''CREATE TABLE IF NOT EXISTS tbl_rank
                      (id INTEGER PRIMARY KEY, time_stamp  integer, date , rank_number integer, role text,champ_id text, rank_filter text,  win_rate real, pick_rate real, ban_rate real)''',
        '''CREATE TABLE IF NOT EXISTS tbl_champion
                      (id INTEGER PRIMARY KEY, english  text, chinese text , chinese_translation text, img_url text)''',
    ]
    for command in migrations:
        run_command(command)
    insert_champion()


def get_all_champions():
    return fetch_all("select id, chinese from tbl_champion")

# create new db, hero to champion, while scraping check data if hero id exist, if not then insert new hero
