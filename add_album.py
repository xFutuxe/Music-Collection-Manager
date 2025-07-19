import tkinter, sqlite3, os, time
from tkinter import messagebox
import main


def addAlbumUI():
    import tkinter.ttk as ttk

    root = tkinter.Tk()
    root.title("Add Album")
    root.geometry("420x520")
    root.configure(bg="#f7f7f7")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", background="#f7f7f7", font=("Segoe UI", 12))
    style.configure("TEntry", font=("Segoe UI", 12))
    style.configure("TButton", font=("Segoe UI", 12), padding=6)
    style.map("TButton", background=[("active", "#0078d7")])

    header = ttk.Label(root, text="Add a New Album", font=("Segoe UI", 18, "bold"), background="#f7f7f7", foreground="#0078d7")
    header.pack(pady=(30, 10))

    fields = ["Album Name", "Artist Name", "Year", "Genre", "Description"]
    entries = {}

    for field in fields:
        frame = ttk.Frame(root)
        frame.pack(fill="x", padx=40, pady=8)
        label = ttk.Label(frame, text=field + ":")
        label.pack(side=tkinter.LEFT, padx=(0, 10))
        entry = ttk.Entry(frame, width=28)
        entry.pack(side=tkinter.RIGHT, fill="x", expand=True)
        entries[field] = entry

    def save_album():
        album_data = {field: entries[field].get() for field in fields}
        try:
            conn = sqlite3.connect(main.DB_FILE)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO users (albumName, artistName, year, genre, decription) VALUES (?, ?, ?, ?, ?)''',
                           (album_data["Album Name"], album_data["Artist Name"], album_data["Year"], album_data["Genre"], album_data["Description"]))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Album added successfully!")
            root.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to add album: {e}")

    save_button = ttk.Button(root, text="Save Album", command=save_album)
    save_button.pack(pady=30)

    root.mainloop()