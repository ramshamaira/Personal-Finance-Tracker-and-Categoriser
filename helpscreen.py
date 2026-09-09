from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image


# Class that controls the entire Help screen layout using Tkinter
class Helpscreen:
    def __init__(self, root):
        self.root = root
        self.window = Toplevel(root)
        self.window.title("Help Screen")
        self.window.geometry("1300x780")
        self.window.config(bg="white")
        self.window.minsize(1300, 780)

      
        #Header section that includes the logo, navigation bar, and search bar for consistency across screens
       
        header_frame = Frame(self.window, bg="white", height=110)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        header_frame.columnconfigure(0, weight=0)
        header_frame.columnconfigure(1, weight=1)
        header_frame.columnconfigure(2, weight=0)

        # Logo
        try:
            logo_img = Image.open("logo copy 2.png")
            logo_img = logo_img.resize((90, 90))
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            Label(header_frame, image=self.logo_photo, bg="white").grid(row=0, column=0, padx=25, sticky="w")
        except:
            Label(header_frame, text="[LOGO]", bg="white", fg="black",
                  width=10, height=4, relief="groove").grid(row=0, column=0, padx=25)

        # Center frame for navigation buttons and search bar
        center_frame = Frame(header_frame, bg="white")
        center_frame.grid(row=0, column=1, sticky="ew")

        # Navigation menu
        nav_frame = Frame(center_frame, bg="white")
        nav_frame.pack(side="left", padx=(20, 10))

        nav_items = ["Dashboard", "Transactions", "Visual Analytics", "Budget", "Help"]
        for item in nav_items:
            Button(nav_frame, text=item, bg="white", fg="black",
                   font=("Arial", 13, "bold"), padx=10, pady=3,
                   relief="groove", bd=1).pack(side="left", padx=6)

        #Search bar 
        search_frame = Frame(center_frame, bg="white")
        search_frame.pack(side="left", padx=(50, 0))

        self.search_entry = Entry(search_frame, width=35, relief="solid", font=("Arial", 11))
        self.search_entry.insert(0, "🔍  Search...")
        self.search_entry.pack(ipady=6)

        # Profile section
        profile_frame = Frame(header_frame, bg="white", width=140, height=90)
        profile_frame.grid(row=0, column=2, padx=25, sticky="e")
        profile_frame.pack_propagate(False)

        try:
            profile_img = Image.open("profile.png")
            profile_img = profile_img.resize((40, 40))
            self.profile_photo = ImageTk.PhotoImage(profile_img)
            Label(profile_frame, image=self.profile_photo, bg="white").pack(pady=(5, 0))
        except:
            Label(profile_frame, text="[Icon]", bg="white", fg="black",
                  width=7, height=3, relief="groove").pack(pady=(5, 0))

        # Profile dropdown menu
        self.profile_menu = Menu(self.window, tearoff=0, bg="white", fg="black", font=("Arial", 11))
        self.profile_menu.add_command(label="My Account")
        self.profile_menu.add_command(label="Settings")
        self.profile_menu.add_separator()
        self.profile_menu.add_command(label="Logout")

        def show_profile_menu(event):
            x = event.widget.winfo_rootx()
            y = event.widget.winfo_rooty() + event.widget.winfo_height()
            self.profile_menu.tk_popup(x, y)

        profile_button = Button(profile_frame, text="Profile ▼", bg="#f2f2f2", fg="black",
                                font=("Arial", 10, "bold"), relief="groove", bd=1,
                                padx=15, pady=5)
        profile_button.pack(pady=(5, 0))
        profile_button.bind("<Button-1>", show_profile_menu)

  
        #Header
       
        content = Frame(self.window, bg="white")
        content.pack(fill="both", expand=True)

        # Title
        Label(content, text="HELP CENTER", bg="white", fg="#333333",
              font=("Arial", 40, "bold")).pack(pady=(35, 25))

        # Big search bar 
        big_search_frame = Frame(content, bg="black")
        big_search_frame.pack(pady=(10, 35))

        # Outer border
        big_search_border = Frame(big_search_frame, bg="black")
        big_search_border.pack()

        big_search_inner = Frame(big_search_border, bg="white")
        big_search_inner.pack(padx=2, pady=2)

        self.help_search = Entry(big_search_inner, width=80, font=("Arial", 16), relief="flat", bg="black")
        self.help_search.insert(0, "How can we help you?")
        self.help_search.pack(ipady=12, padx=12)

        def clear_help_placeholder(event):
            if self.help_search.get() == "  How can we help you?":
                self.help_search.delete(0, END)

        self.help_search.bind("<FocusIn>", clear_help_placeholder)

        # FAQ Label
        faq_frame = Frame(content, bg="white")
        faq_frame.pack(fill="x", padx=220)

        Label(faq_frame, text="FAQ", bg="white", fg="black",
              font=("Arial", 22, "underline")).pack(anchor="w", pady=(0, 15))

        # FAQ dropdown boxes 
        self.faq_items = [
            ("How do I categorize a transaction?",
             "Go to the Transactions screen and use the Category column to assign a category."),
            ("Can I edit a budget?",
             "Yes. Change the limit and category, then save the budget again (edit feature can be added)."),
            ("Where can I view my spending trends?",
             "Go to Visual Analytics to see charts showing category and monthly spending trends.")
        ]

        self.faq_answer_label = Label(content, text="", bg="white", fg="#333333",
                                      font=("Arial", 12), wraplength=900, justify="left")
        
        # (This starts hidden; it will appear after a question is selected)

        for question, answer in self.faq_items:
            row = Frame(faq_frame, bg="white")
            row.pack(fill="x", pady=12)

            box = ttk.Combobox(row, state="readonly", values=[question], font=("Arial", 14))
            box.set(question)
            box.pack(fill="x", ipady=8)

            def on_select(event, ans=answer):
                self.faq_answer_label.config(text=f"Answer: {ans}")
                self.faq_answer_label.pack(pady=(10, 0))

            box.bind("<<ComboboxSelected>>", on_select)

    


# Start the Tkinter application
if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    app = Helpscreen(root)
    root.mainloop()
