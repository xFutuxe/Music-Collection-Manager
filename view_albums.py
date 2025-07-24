import os, time , sqlite3, tkinter
from tkinter import messagebox
import main, db_manager
from PIL import Image, ImageTk

def view_albums(parent):
    def fetch_albums():
        conn = sqlite3.connect(db_manager.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT albumName, artistName, year, genre, decription, albumCoverPath FROM albums")
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
        details_window = tkinter.Toplevel(master=albums_window)
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

        # Show album cover if available
        cover_path = album[5]
        if cover_path and os.path.isfile(cover_path):
            try:
                img = Image.open(cover_path)
                img.thumbnail((200, 200))
                img_tk = ImageTk.PhotoImage(img, master=details_window)
                img_label = tkinter.Label(details_window, image=img_tk)
                img_label.image = img_tk  # Keep reference
                img_label.pack(pady=10)
            except Exception as e:
                error_label = tkinter.Label(details_window, text=f"Could not load album cover: {e}", fg="red")
                error_label.pack()

    def refresh_list():
        global albums
        album_list.delete(0, tkinter.END)
        albums = fetch_albums()
        for album in albums:
            album_list.insert(tkinter.END, f"{album[0]} by {album[1]} ({album[2]})")

    albums_window = tkinter.Toplevel(parent)
    albums_window.title("View Albums")

    album_list = tkinter.Listbox(albums_window, width=50, height=20)
    album_list.pack(padx=10, pady=10)
    album_list.bind('<Double-Button-1>', show_album_details)

    refresh_btn = tkinter.Button(albums_window, text="Refresh", command=refresh_list)
    refresh_btn.pack(pady=5)

    albums = []
    refresh_list()