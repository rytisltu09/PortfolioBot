import sqlite3

def main():
    create_database()

def create_database():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS weather (
                  user_id INTEGER PRIMARY KEY,
                  favorite_city TEXT NOT NULL);''')
    conn.commit()
    conn.close()

def add_favorite_city(user_id, city):
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('''
              INSERT OR REPLACE INTO weather (user_id, favorite_city)
              VALUES (?, ?);''', (user_id, city))
    conn.commit()
    conn.close()

def remove_favorite_city(user_id):
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('''
              DELETE FROM weather WHERE user_id = ?;''', (user_id,))
    conn.commit()
    conn.close()

def get_favorite_city(user_id):
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('''
              SELECT favorite_city FROM weather WHERE user_id = ?;''', (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

if __name__ == "__main__":
    main()