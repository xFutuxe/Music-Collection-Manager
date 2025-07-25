import os, time, sqlite3, tkinter, random
from tkinter import messagebox, filedialog
import db_manager
from PIL import Image, ImageTk


def save_album():

    conn = sqlite3.connect(db_manager.DB_FILE)
    cursor = conn.cursor()

    # Grab values 
    album_name = album_name_entry.get().strip()
    artist_name = artist_entry.get().strip()
    genre = genre_entry.get().strip()
    year = year_entry.get().strip()
    pricing = pricing_entry.get().strip()
    description = description_text.get("1.0", tkinter.END).strip()
    art_path = art_path_var.get().strip()

    if not album_name or not artist_name or not genre or not year:
        messagebox.showerror("Error", "Please fill in all required fields.")
        return
    
    # Generate random ID for album
    album_id = int(time.time() * 1000) 

    # Save album cover to data folder with random name
    if art_path:
        if not os.path.exists(db_manager.DB_FOLDER):
            os.makedirs(db_manager.DB_FOLDER)
        # Use a random name for the album cover

        art_filename = f"{random.getrandbits(128)}.jpg"
        try:
            img = Image.open(art_path_var.get())
            rgb_img = img.convert("RGB")
            # Save album art in data/imgs folder
            imgs_folder = os.path.join(db_manager.DB_FOLDER, "imgs")
            if not os.path.exists(imgs_folder):
                os.makedirs(imgs_folder)
            art_path = os.path.join(imgs_folder, art_filename)
            rgb_img.save(art_path, "JPEG")
            art_path = os.path.abspath(art_path)  # Get absolute path for database storage
        except Exception as e:
            messagebox.showerror("Error", f"Could not save album cover: {e}")
            return

    # Insert album into database
    cursor.execute('''INSERT INTO albums (id, albumName, artistName, year, genre, pricing, description, albumCoverPath) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                   (album_id, album_name, artist_name, year, genre, pricing, description, art_path))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Album saved successfully!")



def addAlbumUI(root, main_menu_frame):

    global album_name_entry, artist_entry, genre_entry, year_entry, pricing_entry, description_text, art_path_var

    # Hide the main menu frame
    main_menu_frame.pack_forget()

    # Remove any existing add_album_frame
    for widget in root.winfo_children():
        if isinstance(widget, tkinter.Frame) and widget != main_menu_frame:
            widget.pack_forget()

    # Create the Add Album frame
    add_album_frame = tkinter.Frame(root, bg="#DDDDDD")
    add_album_frame.pack(fill="both", expand=True)

    # Title
    title_label = tkinter.Label(
        add_album_frame, text="Add Album", font=("Segoe UI", 18, "bold"),
        fg="black", bg="#DDDDDD"
    )
    title_label.grid(row=0, column=0, columnspan=4, pady=(20, 8), sticky="n")

    entry_width = 25
    padx = 30
    pady_label = 4
    pady_entry = (0, 10)

    # First Column
    album_name_label = tkinter.Label(
        add_album_frame, text="Album Name:", font=("Segoe UI", 11),
        fg="black", bg="#DDDDDD", anchor="w"
    )
    album_name_label.grid(row=1, column=0, sticky="w", padx=padx, pady=(0, pady_label))
    album_name_entry = tkinter.Entry(
        add_album_frame, font=("Segoe UI", 11),
        bg="#FFFFFF", fg="black", insertbackground="black",  # <-- changed to black
        width=entry_width, cursor="xterm"
    )
    album_name_entry.grid(row=2, column=0, sticky="ew", padx=padx, pady=pady_entry)

    artist_label = tkinter.Label(
        add_album_frame, text="Artist:", font=("Segoe UI", 11),
        fg="black", bg="#DDDDDD", anchor="w"
    )
    artist_label.grid(row=3, column=0, sticky="w", padx=padx, pady=(0, pady_label))
    artist_entry = tkinter.Entry(
        add_album_frame, font=("Segoe UI", 11),
        bg="#FFFFFF", fg="black", insertbackground="black",
        width=entry_width
    )
    artist_entry.grid(row=4, column=0, sticky="ew", padx=padx, pady=pady_entry)

    genre_label = tkinter.Label(
        add_album_frame, text="Genre:", font=("Segoe UI", 11),
        fg="black", bg="#DDDDDD", anchor="w"
    )
    genre_label.grid(row=5, column=0, sticky="w", padx=padx, pady=(0, pady_label))
    genre_entry = tkinter.Entry(
        add_album_frame, font=("Segoe UI", 11),
        bg="#FFFFFF", fg="black", insertbackground="black",  
        width=entry_width
    )
    genre_entry.grid(row=6, column=0, sticky="ew", padx=padx, pady=pady_entry)

    # Second Column
    year_label = tkinter.Label(
        add_album_frame, text="Year:", font=("Segoe UI", 11),
        fg="black", bg="#DDDDDD", anchor="w"
    )
    year_label.grid(row=1, column=1, sticky="w", padx=padx, pady=(0, pady_label))
    year_entry = tkinter.Entry(
        add_album_frame, font=("Segoe UI", 11),
        bg="#FFFFFF", fg="black", insertbackground="black",  
        width=entry_width
    )
    year_entry.grid(row=2, column=1, sticky="ew", padx=padx, pady=pady_entry)

    pricing_label = tkinter.Label(
        add_album_frame, text="Pricing (optional)", font=("Segoe UI", 11),
        fg="black", bg="#DDDDDD", anchor="w"
    )
    pricing_label.grid(row=3, column=1, sticky="w", padx=padx, pady=(0, pady_label))
    pricing_entry = tkinter.Entry(
        add_album_frame, font=("Segoe UI", 11),
        bg="#FFFFFF", fg="black", insertbackground="black",  
        width=entry_width
    )
    pricing_entry.grid(row=4, column=1, sticky="ew", padx=padx, pady=pady_entry)

    art_label = tkinter.Label(
        add_album_frame, text="Album Art (optional):", font=("Segoe UI", 11),
        fg="black", bg="#DDDDDD", anchor="w"
    )
    art_label.grid(row=5, column=1, sticky="w", padx=padx, pady=(0, pady_label))

    art_path_var = tkinter.StringVar()

    def browse_art():
        file_path = filedialog.askopenfilename(
            title="Select Album Art",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
        )
        if file_path:
            art_path_var.set(file_path)

    art_browse_frame = tkinter.Frame(add_album_frame, bg="#DDDDDD")
    art_browse_frame.grid(row=6, column=1, sticky="ew", padx=padx, pady=pady_entry)

    art_path_entry = tkinter.Entry(
        art_browse_frame, textvariable=art_path_var, font=("Segoe UI", 11),
        bg="#FFFFFF", fg="black", insertbackground="black",  
        width=entry_width-7, state="readonly"
    )
    art_path_entry.pack(side="left", fill="x", expand=True)

    browse_btn = tkinter.Button(
        art_browse_frame, text="Browse...", font=("Segoe UI", 10),
        bg="#7289DA", fg="white", activebackground="#99AAB5", activeforeground="white",
        bd=0, width=8, cursor="hand2", command=browse_art
    )
    browse_btn.pack(side="left", padx=(6, 0))

    # Description (spans both columns)
    description_label = tkinter.Label(
        add_album_frame, text="Description:", font=("Segoe UI", 11),
        fg="black", bg="#DDDDDD", anchor="w"
    )
    description_label.grid(row=7, column=0, columnspan=2, sticky="w", padx=padx, pady=(0, pady_label))
    description_text = tkinter.Text(
        add_album_frame, font=("Segoe UI", 11),
        bg="#FFFFFF", fg="black", insertbackground="black", 
        height=3, width=60
    )
    description_text.grid(row=8, column=0, columnspan=2, sticky="ew", padx=padx, pady=pady_entry)

    # Buttons (centered below)
    button_frame = tkinter.Frame(add_album_frame, bg="#DDDDDD")
    button_frame.grid(row=9, column=0, columnspan=2, pady=18)

    save_btn = tkinter.Button(
        button_frame, text="Save Album", font=("Segoe UI", 11, "bold"),
        bg="#7289DA", fg="white", activebackground="#99AAB5", activeforeground="white",
        bd=0, width=13, cursor="hand2", command=lambda : save_album()
    )
    save_btn.pack(side="left", padx=8)

    cancel_btn = tkinter.Button(
        button_frame, text="Cancel", font=("Segoe UI", 11, "bold"),
        bg="#99AAB5", fg="white", activebackground="#23272A", activeforeground="white",
        bd=0, width=13, cursor="hand2",
        command=lambda: [add_album_frame.pack_forget(), main_menu_frame.pack(fill="both", expand=True)]
    )
    cancel_btn.pack(side="left", padx=8)

    # Make columns expand evenly
    add_album_frame.grid_columnconfigure(0, weight=1)
    add_album_frame.grid_columnconfigure(1, weight=1)

    return add_album_frame


