import tkinter, sqlite3, os, time
from tkinter import messagebox, filedialog
import db_manager
import shutil


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

    def select_cover():
        file_path = tkinter.filedialog.askopenfilename(
            title="Select Album Cover",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
        )
        if file_path:
            entries["Album Cover"].delete(0, tkinter.END)
            entries["Album Cover"].insert(0, file_path)

    cover_frame = ttk.Frame(root)
    cover_frame.pack(fill="x", padx=40, pady=8)
    cover_btn = ttk.Button(cover_frame, text="Browse...", command=select_cover)
    cover_btn.pack(side=tkinter.RIGHT, padx=(10, 0))

    def save_album():
        if not validate_fields():
            return
        album_data = {field: entries[field].get() for field in fields}
        cover_src = album_data["Album Cover"]
        cover_dest = ""
        if cover_src and os.path.isfile(cover_src):
            ext = os.path.splitext(cover_src)[1]
            safe_name = f"{int(time.time())}_{os.path.basename(cover_src)}"
            imgs_dir = os.path.join("data", "imgs")
            os.makedirs(imgs_dir, exist_ok=True)
            cover_dest = os.path.join(imgs_dir, safe_name)
            try:
                shutil.copy2(cover_src, cover_dest)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to copy album cover: {e}")
                return
        else:
            cover_dest = ""
        try:
            conn = sqlite3.connect(db_manager.DB_FILE)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO albums (albumName, artistName, year, genre, decription, albumCover) VALUES (?, ?, ?, ?, ?, ?)''',
                           (album_data["Album Name"], album_data["Artist Name"], album_data["Year"], album_data["Genre"], album_data["Description"], cover_dest))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Album added successfully!")
            root.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to add album: {e}")

    def validate_fields():
        for field in fields:
            if not entries[field].get().strip():
                messagebox.showerror("Input Error", f"{field} cannot be empty.")
                return False
        return True

    def save_album():
        if not validate_fields():
            return  # Stop if validation fails
        album_data = {field: entries[field].get() for field in fields}
        try:
            conn = sqlite3.connect(db_manager.DB_FILE)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO albums (albumName, artistName, year, genre, decription) VALUES (?, ?, ?, ?, ?)''',
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