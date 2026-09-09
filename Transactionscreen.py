from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import json
import VisualAnalysticsfinal as vas
import Dashboardscreen as dash

# Main class for creating and controlling the Transaction screen.
# All widgets and functions for this screen are grouped together
# so the layout, filtering, and table display can be maintained
# or updated easily without affecting other screens.
class Transaction:
	# The Transaction class is responsible for displaying transaction data,
    # allowing the user to filter and search transactions, and masking
    # transaction amounts when privacy is needed.
    def __init__(self, root):
		# Store root window reference so other screens can be opened later
        self.window = Toplevel(root)
        self.root = root
        self.window.title("Transaction")
        self.window.geometry("1300x780")
        self.window.config(bg="white")
        self.window.minsize(1300, 780)
        
        # Boolean variable used to track whether amounts are visible or masked.
        # Keeping this as a separate variable makes it easier to extend
        # the privacy feature later if needed.
        self.mask_amounts = False

        # Header frame: This section contains logo, navigation menu, and search bar
        # Keeping these elements together creates a consistent header layout
        # that can easily be reused on other screens.
        header_frame = Frame(self.window, bg="white", height=110)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        header_frame.columnconfigure(0, weight=0)
        header_frame.columnconfigure(1, weight=1)
        header_frame.columnconfigure(2, weight=0)

        # Logo on the left(resized to fit better into layout)
        # Attempt to load the logo image. If the image file is missing,
        # a placeholder label is displayed instead so the program continues
        # running without crashing.
        try:
            logo_img = Image.open("logo copy 2.png")
            logo_img = logo_img.resize((90, 90))
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            Label(header_frame, image=self.logo_photo, bg="white").grid(row=0, column=0, padx=25, sticky="w")
        except:
            Label(header_frame, text="[LOGO]", bg="white",
                  width=10, height=4, relief="groove").grid(row=0, column=0, padx=25)

        # Centre frame for navigation buttons and search bar
        # Grouping these elements makes the top section easier to align and maintain.
        center_frame = Frame(header_frame, bg="white")
        center_frame.grid(row=0, column=1, sticky="ew")

        # Navigation menu on the right – allows user to explore other screens
        # Navigation options are generated using a loop so additional
        # menu items can be added later without rewriting the code.
        nav_frame = Frame(center_frame, bg="white")
        nav_frame.pack(side="left", padx=(20, 10))
        nav_items = ["Dashboard", "Transactions", "Visual Analytics", "Budget", "Help"]
        for item in nav_items:
            Button(nav_frame, text=item, bg="white", fg="black",
                   font=("Arial", 13, "bold"), padx=10, pady=3,
                   relief="groove", bd=1,
                   command=lambda name=item: self.top_navgiation_button_click(name)).pack(side="left", padx=6)

        # Search bar is included for interface consistency with the
        # rest of the application. It could be extended later to support
        # wider application search functionality.
        search_frame = Frame(center_frame, bg="white")
        search_frame.pack(side="left", padx=(50, 0))
        self.search_entry = Entry(search_frame, width=35, relief="solid", font=("Arial", 11))
        self.search_entry.insert(0, "🔍  Search...")
        self.search_entry.pack(ipady=6)

        # Profile section placed on the right of the header.
        # Keeping this in a separate frame makes the account area easier
        # to position consistently on all screens.
        profile_frame = Frame(header_frame, bg="white", width=140, height=90)
        profile_frame.grid(row=0, column=2, padx=25, sticky="e")
        profile_frame.pack_propagate(False)

        try:
            profile_img = Image.open("profile.png")
            profile_img = profile_img.resize((40, 40))
            self.profile_photo = ImageTk.PhotoImage(profile_img)
            Label(profile_frame, image=self.profile_photo, bg="white").pack(pady=(5, 0))
        except:
            Label(profile_frame, text="[Icon]", bg="white",
                  width=7, height=3, relief="groove").pack(pady=(5, 0))

        # Profile dropdown menu
        # This calculates where the menu should appear so that the
        # dropdown opens directly below the profile button.
        def show_profile_menu(event):
            x = event.widget.winfo_rootx()
            y = event.widget.winfo_rooty() + event.widget.winfo_height()
            self.profile_menu.tk_popup(x, y)
        
        # Profile button used to open the dropdown menu.
        profile_button = Button(profile_frame, text="Profile ▼", bg="#f2f2f2",
                                font=("Arial", 10, "bold"), relief="groove",
                                padx=15, pady=5)
        profile_button.pack(pady=(5, 0))
        
        # Dropdown menu containing account-related action
        self.profile_menu = Menu(self.window, tearoff=0)
        self.profile_menu.add_command(label="My Account")
        self.profile_menu.add_command(label="Settings")
        self.profile_menu.add_separator()
        self.profile_menu.add_command(label="Logout")
        profile_button.bind("<Button-1>", show_profile_menu)

        # Load transaction data from JSON file
        # Validation is applied here to ensure the file structure is valid
        # and that only complete and usable transaction data is stored.
        try:
            with open("data.json", "r") as file:
                data = json.load(file)

            # Validation: check that the JSON file contains the
            # expected "transactions" key before reading the data.
            if "transactions" not in data:
                raise ValueError("Invalid JSON structure: 'transactions' key missing")

            self.transactions = []

            for t in data["transactions"]:
				# Validation: each transaction should be stored as a dictionary
                if not isinstance(t, dict):
                    continue
                # Validation: required fields must exist
                if "date" not in t or "description" not in t or "amount" not in t or "category" not in t:
                    continue

                # Validation: amount must be a valid positive number
                try:
                    amount = float(t["amount"])
                    if amount <= 0:
                        continue
                except (ValueError, TypeError):
                    continue

                self.transactions.append(t)

        except Exception:
            messagebox.showwarning(
                "Data Error",
                "Transaction file is missing or invalid. Backup data has been loaded."
            )
			
            # Backup data if file not found
            # This prevents the application from failing completely and
            # allows the screen to continue running for demonstration purposes.
            self.transactions = [
                {"date": "01/01/2026", "description": "Tesco - Groceries", "amount": 10.0, "category": "Food"},
                {"date": "02/01/2026", "description": "Amazon - Online order", "amount": 15.0, "category": "Shopping"},
            ]

        # Main frame
        # This frame groups together the headings, controls, and table
        # so that the screen structure is easier to manage
        main_frame = Frame(self.window, bg="white")
        main_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # Headings row showing quick summary titles.
        # These labels give the user a clear overview of the key information
        # presented on this screen
        stats_frame = Frame(main_frame, bg="white")
        stats_frame.pack(fill="x", pady=(10, 15))

        Label(stats_frame, text="Total Spend this Month", bg="white", font=("Arial", 14)).pack(side="left", expand=True)
        Label(stats_frame, text="Number of Transactions", bg="white", font=("Arial", 14)).pack(side="left", expand=True)
        Label(stats_frame, text="Most Frequent Category", bg="white", font=("Arial", 14)).pack(side="left", expand=True)

        # Filters section
        # This area holds the dropdown filters and search controls used
        # to narrow down the visible transactions in the table.
        controls_frame = Frame(main_frame, bg="white")
        controls_frame.pack(fill="x", pady=(10, 20))

        # Date filter allows users to choose a date range.
        self.date_filter = ttk.Combobox(controls_frame, state="readonly", width=18,
                                        values=["All Dates", "This Month", "Last Month"])
        self.date_filter.set("All Dates")
        self.date_filter.pack(side="left", padx=(0, 20), ipady=6)

        # Category filter allows transactions to be filtered by category.
        # Readonly mode prevents invalid manual entries.
        self.category_filter = ttk.Combobox(controls_frame, state="readonly", width=18,
                                            values=["All Categories", "Food", "Transport", "Shopping", "Entertainment"])
        self.category_filter.set("All Categories")
        self.category_filter.pack(side="left", padx=(0, 30), ipady=6)
        # Description search entry.
        # This lets the user search transactions using text from the
        # description field.
        self.desc_search = Entry(controls_frame, width=35, relief="solid", font=("Arial", 11))
        self.desc_search.insert(0, "🔍  Search by description")
        self.desc_search.pack(side="left", padx=(0, 30), ipady=8)

        # Clear placeholder when user clicks inside the search box
        # This makes the field easier to use and avoids confusion.
        def clear_placeholder(event):
            if self.desc_search.get() == "🔍  Search by description":
                self.desc_search.delete(0, END)

        self.desc_search.bind("<FocusIn>", clear_placeholder)
        # Search button applies the current category and description filters.
        Button(controls_frame, text="Search", font=("Arial", 14),
               relief="groove", padx=60, command=self.apply_filters).pack(side="right")
        
        # Toggle Mask button allows the user to hide or reveal transaction amounts.
        # This supports privacy when financial data is visible on screen.      
        Button(controls_frame,text="Toggle Mask",font=("Arial", 12),command=self.toggle_mask).pack(side="right", padx=10)


        # Transaction table section
        #A Treeview is used because it allows transaction data to be shown
        # clearly in rows and columns, which is suitable for financial records.
        table_frame = Frame(main_frame, bg="white")
        table_frame.pack(fill="both", expand=True)

        columns = ("date", "description", "amount", "category")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=14)

        # Table headings
        self.table.heading("date", text="Date")
        self.table.heading("description", text="Description")
        self.table.heading("amount", text="Amount")
        self.table.heading("category", text="Category")

        # Column sizes are set manually to improve readability
        # and keep the layout balanced.
        self.table.column("date", width=140)
        self.table.column("description", width=450)
        self.table.column("amount", width=120)
        self.table.column("category", width=200)

        self.table.pack(side="left", fill="both", expand=True)
        
        # Vertical scrollbar allows the table to handle larger sets of data
        # without the interface becoming cluttered.
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        scrollbar.pack(side="right", fill="y")
        self.table.configure(yscrollcommand=scrollbar.set)

        # Display transactions in table
        self.populate_table(self.transactions)

    # Populates the transaction table with the supplied transaction list.
    # The function is kept separate so it can be reused after filtering
    # or masking actions without rewriting the display code.
    def populate_table(self, tx_list):
        self.table.delete(*self.table.get_children())
        
        
        for t in tx_list:
			# Validation: ensure important fields exist before displaying
            date = t.get("date", "")
            description = t.get("description", "")
            category = t.get("category", "")

            if date == "" or description == "":
                continue
            amount = float(t.get("amount", 0))


            # If masking is enabled, the real amount is hidden from view.
            if self.mask_amounts:
                display_amount = "£****"
            else:
                display_amount = f"£{amount:.2f}"

            self.table.insert("", "end", values=(
                t.get("date", ""),
                t.get("description", ""),
                display_amount,
                t.get("category", "")
            ))                 
    # This switches between showing and hiding transaction amounts.
    # The table is then refreshed so that the change appears immediately.       
    def toggle_mask(self):
        self.mask_amounts = not self.mask_amounts
        self.populate_table(self.transactions)

    # Apply filters based on category and description
    # This function allows users to narrow down the list of transactions
    # using the selected category and the search text entered.
    def apply_filters(self):
        category = self.category_filter.get()
        # Validation: ensure the selected category is one of the valid options
        valid_categories = ["All Categories", "Food", "Transport", "Shopping", "Entertainment"]
        if category not in valid_categories:
            messagebox.showerror("Filter Error", "Invalid category selected.")
            return

        # Remove placeholder text before filtering( search option)
        search_text = self.desc_search.get().strip().lower()
        if search_text == "🔍  search by description":
            search_text = ""
            
         # Limit search input length so extremely long inputs are not processed
        if len(search_text) > 50:
            messagebox.showwarning("Search Error", "Search text is too long.")
            return

        filtered = []
        for t in self.transactions:
            if category != "All Categories" and t.get("category", "") != category:
                continue

            if search_text and search_text not in str(t.get("description", "")).lower():
                continue

            filtered.append(t)
        
        # Repopulate the table with the filtered results
        self.populate_table(filtered)      
       
       # Top navigation on click event
       # This function controls movement between screens based on
       # the button selected in the navigation bar.
    def top_navgiation_button_click(self, name):
        if name == "Visual Analytics":
            vas.VisualAnalyticsApp(self.root)
        
        elif name == "Dashboard":
            dash.DashboardApp(self.root)         

        else:
            messagebox.showinfo("Navigation", f"{name} screen will be added next.")


# Start the Tkinter application
if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    app = Transaction(root)
    root.mainloop()
