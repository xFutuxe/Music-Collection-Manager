import tkinter
import add_album, view_albums
import db_manager

def mainMenu():
    root = tkinter.Tk()
    root.title("Music Collection")
    root.geometry("500x600")
    
    menubar = tkinter.Menu(root)
    menu = tkinter.Menu(menubar, tearoff=0)
    menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="Menu", menu=menu)

    tools_menu = tkinter.Menu(menubar, tearoff=0)
    tools_menu.add_command(label="Coming Soon")
    menubar.add_cascade(label="Tools", menu=tools_menu)

    root.config(menu=menubar)

    label = tkinter.Label(root, text="Welcome to your Music Collection", font=("Arial", 16))
    label.pack(pady=20)
    
    status_text = db_manager.check_database_integrity()


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

    btnAddAlbum = tkinter.Button(root, text="Add Album", command=lambda: add_album.addAlbumUI(), **button_style)
    btnAddAlbum.pack(pady=15)
    btnViewAlbums = tkinter.Button(root, text="View Albums", command=lambda: view_albums.view_albums(), **button_style)
    btnViewAlbums.pack(pady=15)
    btnSearchAlbum = tkinter.Button(root, text="Search Album", command=lambda: print("Search Albums"), **button_style)
    btnSearchAlbum.pack(pady=15)
    btnExit = tkinter.Button(root, text="Exit", command=root.quit, **button_style)
    btnExit.pack(pady=15)


    root.mainloop()
    

def main():
    db_manager.initialize_database()
    mainMenu()

if __name__ == "__main__":
    main()