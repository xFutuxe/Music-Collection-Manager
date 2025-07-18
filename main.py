import tkinter, sqlite3, os, time

DB_FILE = "collection.db"

def database():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, albumName TEXT, artistName TEXT, year INTEGER, genre TEXT, decription TEXT)''')
        conn.commit()
        conn.close()

def mainMenu():
    root = tkinter.Tk()
    root.title("Music Collection")
    root.geometry("500x600")
    
    label = tkinter.Label(root, text="Welcome to your Music Collection", font=("Arial", 16))
    label.pack(pady=20)
    
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


    uiStatusBar = tkinter.Label(root, text=status_text, bd=1, relief=tkinter.SUNKEN, anchor=tkinter.E)
    uiStatusBar.pack(side=tkinter.BOTTOM, fill=tkinter.X, ipadx=5, ipady=5)

     # Hide "Integrity check passed" after 5 seconds
    if status_text == "Connected to database! Integrity check passed.":
        def clear_status():
            uiStatusBar.config(text="Connected to Database!")
        root.after(5000, clear_status)

    
    # Menu Buttons
    button_style = {
        "font": ("Segoe UI", 14, "bold"),
        "bg": "#4CAF50",
        "fg": "white",
        "activebackground": "#388E3C",
        "activeforeground": "white",
        "bd": 0,
        "height": 2,
        "width": 20,
        "cursor": "hand2"
    }

    btnAddAlbum = tkinter.Button(root, text="Add Album", command=lambda: print("Add Album clicked"), **button_style)
    btnAddAlbum.pack(pady=15)
    btnViewAlbums = tkinter.Button(root, text="View Albums", command=lambda: print("View Albums clicked"), **button_style)
    btnViewAlbums.pack(pady=15)
    btnSearchAlbum = tkinter.Button(root, text="Search Album", command=lambda: print("Search Album clicked"), **button_style)
    btnSearchAlbum.pack(pady=15)
    btnExit = tkinter.Button(root, text="Exit", command=root.quit, **button_style)
    btnExit.pack(pady=15)


    root.mainloop()
    

def main():
    database()
    mainMenu()

if __name__ == "__main__":
    main()