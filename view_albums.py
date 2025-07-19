import os, time , sqlite3, tkinter
from tkinter import messagebox
import main, db_manager

def view_albums():
    def fetch_albums():
        conn = sqlite3.connect(db_manager.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT albumName, artistName, year, genre, decription FROM albums")
        albums = cursor.fetchall()
        conn.close()
        return albums

    def show_album_details(event):
        global albums
        selection = album_list.curselection()
        if not selection:
            return
        index = selection[0]
        album = albums[index]
        details_window = tkinter.Toplevel(root)
        details_window.title(f"Album Details - {album[0]}")
        info = (
            f"Album Name: {album[0]}\n"
            f"Artist Name: {album[1]}\n"
            f"Year: {album[2]}\n"
            f"Genre: {album[3]}\n"
            f"Description: {album[4]}"
        )
        label = tkinter.Label(details_window, text=info, justify="left", padx=10, pady=10)
        label.pack()

    def refresh_list():
        global albums
        album_list.delete(0, tkinter.END)
        albums = fetch_albums()
        for album in albums:
            album_list.insert(tkinter.END, f"{album[0]} by {album[1]} ({album[2]})")

    root = tkinter.Tk()
    root.title("View Albums")

    album_list = tkinter.Listbox(root, width=50, height=20)
    album_list.pack(padx=10, pady=10)
    album_list.bind('<Double-Button-1>', show_album_details)

    refresh_btn = tkinter.Button(root, text="Refresh", command=refresh_list)
    refresh_btn.pack(pady=5)

    albums = []
    refresh_list()
    root.mainloop()