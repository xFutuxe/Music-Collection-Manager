import tkinter, sqlite3, os, time
from tkinter import messagebox, filedialog
import db_manager
import shutil


def addAlbumUI(root, main_menu_frame):
    import tkinter.ttk as ttk

    # Hide main menu frame
    main_menu_frame.pack_forget()

    # Create add album frame
    add_album_frame = ttk.Frame(root)
    add_album_frame.pack(fill="both", expand=True)
    add_album_frame.configure(style="TFrame")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", background="#f7f7f7", font=("Segoe UI", 12))
    style.configure("TEntry", font=("Segoe UI", 12))
    style.configure("TButton", font=("Segoe UI", 12), padding=6)
    style.map("TButton", background=[("active", "#0078d7")])

    header = ttk.Label(add_album_frame, text="Add a New Album", font=("Segoe UI", 18, "bold"), background="#f7f7f7", foreground="#0078d7")
    header.pack(pady=(30, 10))

    fields = ["Album Name", "Artist Name", "Year", "Genre", "Description", "Album Cover"]
    entries = {}

    def select_cover():
        file_path = filedialog.askopenfilename(
            title="Select Album Cover",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
        )
        if file_path:
            entries["Album Cover"].delete(0, tkinter.END)
            entries["Album Cover"].insert(0, file_path)

    for field in fields:
        if field == "Album Cover":
            frame = ttk.Frame(add_album_frame)
            frame.pack(fill="x", padx=40, pady=8)
            label = ttk.Label(frame, text=field + ":")
            label.pack(side=tkinter.LEFT, padx=(0, 10))
            # Hide entry, only show button and status label
            upload_status = ttk.Label(frame, text="No image uploaded", foreground="#888")
            upload_status.pack(side=tkinter.RIGHT, padx=(10, 0))
            def select_cover():
                file_path = filedialog.askopenfilename(
                    title="Select Album Cover",
                    filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
                )
                if file_path:
                    entries["Album Cover"] = file_path
                    upload_status.config(text="Image uploaded!", foreground="#0078d7")
                else:
                    upload_status.config(text="No image uploaded", foreground="#888")
            cover_btn = ttk.Button(frame, text="Browse...", command=select_cover)
            cover_btn.pack(side=tkinter.RIGHT, padx=(10, 0))
        else:
            frame = ttk.Frame(add_album_frame)
            frame.pack(fill="x", padx=40, pady=8)
            label = ttk.Label(frame, text=field + ":")
            label.pack(side=tkinter.LEFT, padx=(0, 10))
            entry = ttk.Entry(frame, width=28)
            entry.pack(side=tkinter.RIGHT, fill="x", expand=True)
            entries[field] = entry

    def validate_fields():
        for field in fields[:-1]:  # Don't require Album Cover
            if not entries[field].get().strip():
                messagebox.showerror("Input Error", f"{field} cannot be empty.")
                return False
        return True

    def save_album():
        if not validate_fields():
            return
        album_data = {}
        for field in fields:
            if field == "Album Cover":
                album_data[field] = entries.get(field, "")
            else:
                album_data[field] = entries[field].get()
        cover_src = album_data["Album Cover"]
        cover_dest = ""
        if cover_src and os.path.isfile(cover_src):
            import uuid
            ext = os.path.splitext(cover_src)[1]
            random_name = f"{uuid.uuid4().hex}{ext}"
            imgs_dir = os.path.join("data", "imgs")
            os.makedirs(imgs_dir, exist_ok=True)
            cover_dest = os.path.join(imgs_dir, random_name)
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
            cursor.execute('''INSERT INTO albums (albumName, artistName, year, genre, decription, albumCoverPath) VALUES (?, ?, ?, ?, ?, ?)''',
                           (album_data["Album Name"], album_data["Artist Name"], album_data["Year"], album_data["Genre"], album_data["Description"], cover_dest))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Album added successfully!")
            back_to_main()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to add album: {e}")

    def back_to_main():
        add_album_frame.pack_forget()
        main_menu_frame.pack(fill="both", expand=True)

    save_button = ttk.Button(add_album_frame, text="Save Album", command=save_album)
    save_button.pack(pady=20)

    back_button = ttk.Button(add_album_frame, text="Back", command=back_to_main)
    back_button.pack(pady=10)