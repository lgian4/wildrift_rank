import sqlite3


def save_list_to_sqlite(list):
    conn = sqlite3.connect('database.db')
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
    conn = sqlite3.connect('database.db')
    try:
        cursor = conn.cursor()
        cursor.execute(command)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error executing command: {command}\nError message: {e}")
    finally:
        conn.close()


def fetch_one(command):
    conn = sqlite3.connect('database.db')
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
    migrations = [
        '''CREATE TABLE IF NOT EXISTS tbl_ranking

                      (id INTEGER PRIMARY KEY, time_stamp  integer, date , rank_number integer, role text,hero_img_url text, hero_name text, rank_filter text,  win_rate real, pick_rate real, ban_rate real)''',
        '''ALTER TABLE tbl_ranking ADD COLUMN  created_at TIMESTAMP ''']
    for command in migrations:
        run_command(command)

