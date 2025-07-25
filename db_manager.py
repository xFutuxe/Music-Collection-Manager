import os
import sqlite3
import main

DB_FOLDER = "data"
DB_FILE = os.path.join(DB_FOLDER, "collection.db")

def initialize_database():
    # Create the folder if it doesn't exist
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS albums (id INTEGER PRIMARY KEY, albumName TEXT, artistName TEXT, year INTEGER, genre TEXT, pricing TEXT, decription TEXT, albumCoverPath BLOB)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS tracks (id INTEGER PRIMARY KEY, albumId INTEGER, trackName TEXT, duration TEXT, FOREIGN KEY(albumId) REFERENCES albums(id))''')
        conn.commit()
        conn.close()

def check_database_integrity():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check;")
        result = cursor.fetchone()
        if result[0] != "ok":
            status_text = "Database integrity check failed!"
            cursor.close()
            conn.close()
            raise sqlite3.DatabaseError(status_text)
        else:
            status_text = "Connected to database! Integrity check passed."
        cursor.close()
        conn.close()
    except sqlite3.Error:
        status_text = "Failed to connect to database!"
    return status_text
