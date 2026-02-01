
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import json  

#Class that creates the Dashboard screen layout and functionality using Tkinter
class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1300x780")
        self.root.config(bg="white")

        # top frame for page label
        top_frame = Frame(self.root, bg="lightgrey", height=40)
        top_frame.pack(fill="x")
        Label(top_frame, text="Dashboard Screen", bg="lightgrey",
              font=("Arial", 10, "bold")).pack(side="left", padx=10)

      
        # Load data from JSON file
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
            self.transactions = data["transactions"]
        except:
            self.transactions = []
            messagebox.showerror("Error", "Could not load data.json")

        # To calculate values for the titles
        self.monthly_total = sum(t["amount"] for t in self.transactions)
        self.demo_budget = 1500
        self.remaining_budget = self.demo_budget - self.monthly_total

        self.category_totals = {}
        for t in self.transactions:
            cat = t["category"]
            self.category_totals[cat] = self.category_totals.get(cat, 0) + t["amount"]

       
        #Header frame
        header_frame = Frame(self.root, bg="white")
        header_frame.pack(fill="x", pady=(10, 0))

        #Logo on the left
        try:
            logo_img = Image.open("logo copy 2.png")
            logo_img = logo_img.resize((90, 90))
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            Label(header_frame, image=self.logo_photo,
                  bg="white").pack(side="left", padx=25)
        except:
            Label(header_frame, text="[LOGO]", bg="white",
                  fg="black", width=10, height=4,
                  relief="groove").pack(side="left", padx=25)

        # Navigation bar
        nav_frame = Frame(header_frame, bg="white")
        nav_frame.pack(side="left", padx=40)

        nav_items = ["Dashboard", "Transactions", "Visual Analytics", "Budget", "Help"]
        for item in nav_items:
            Button(nav_frame, text=item, bg="white", fg="black",
                   font=("Arial", 13, "bold"), padx=10, pady=5,
                   width=5, relief="groove", bd=1).pack(side="left", padx=8)

        # Search bar
        search_frame = Frame(header_frame, bg="white")
        search_frame.pack(side="left", padx=50)
        self.search_entry = Entry(search_frame, width=40, relief="solid",
                                  font=("Arial", 11))
        self.search_entry.insert(0, "🔍  Search...")
        self.search_entry.pack(ipady=6)

        # Profile setting
        profile_frame = Frame(header_frame, bg="white")
        profile_frame.pack(side="right", padx=25)
        try:
            profile_img = Image.open("profile.png")
            profile_img = profile_img.resize((40, 40))
            self.profile_photo = ImageTk.PhotoImage(profile_img)
            Label(profile_frame, image=self.profile_photo,
                  bg="white").pack()
        except:
            Label(profile_frame, text="[Icon]", bg="white",
                  fg="black", width=7, height=3,
                  relief="groove").pack()
                  
            #profile button
        def show_profile_menu(event):
            x = event.widget.winfo_rootx()
            y = event.widget.winfo_rooty() + event.widget.winfo_height()
            self.profile_menu.tk_popup(x, y)

        profile_button = Button(profile_frame, text="Profile ▼", bg="#f2f2f2", fg="black",
                                font=("Arial", 10, "bold"), relief="groove", bd=1,
                                padx=15, pady=5)
        profile_button.pack(pady=(5, 0))

        #dropdown menu
        self.profile_menu = Menu(self.root, tearoff=0, bg="white", fg="black", font=("Arial", 11))
        self.profile_menu.add_command(label="My Account", command=lambda: messagebox.showinfo("Profile", "Opening account settings..."))
        self.profile_menu.add_command(label="Settings", command=lambda: messagebox.showinfo("Profile", "Opening settings..."))
        self.profile_menu.add_separator()
        self.profile_menu.add_command(label="Logout", command=lambda: messagebox.showinfo("Logout", "You have been logged out!"))

        profile_button.bind("<Button-1>", show_profile_menu)
        self.profile_menu.config(activebackground="#f2f2f2", activeforeground="black", bd=1)

        #To update the geometric size
        self.root.update()

        # Tiles Section
        tiles_frame = Frame(self.root, bg="white")
        tiles_frame.pack(pady=20)

        tile_titles = [
            "Current Monthly Spending",
            "Remaining Budget",
            "Categorized Expenditure Summaries"
        ]

        tile_colors = ["#B76B50", "#DC380C", "#DD440F"]

        tile_values = [
            f"£{self.monthly_total}",
            f"£{self.remaining_budget}",
            ", ".join([f"{k}: £{v}" for k, v in self.category_totals.items()])
        ]

        for i in range(3):
            tile = Frame(tiles_frame, bg=tile_colors[i],
                         width=400, height=200,
                         relief="solid", bd=1)
            tile.pack(side="left", padx=30)
            tile.pack_propagate(False)

            Label(tile, text=tile_titles[i], font=("Arial", 12, "italic"),
                  bg=tile_colors[i]).pack(pady=(25, 10))

            Label(tile, text=tile_values[i], bg=tile_colors[i],
                  font=("Arial", 12, "bold"),
                  wraplength=350).pack()
   
        # Summary Section
        summary_frame = Frame(self.root, bg="black")
        summary_frame.pack(fill="both", expand=True,
                           padx=40, pady=(30, 30), ipady=30)

        Label(summary_frame, text="Recent Activity Summary",
              bg="black", fg="white", font=("Arial", 18, "bold"),
              anchor="w").pack(fill="x", padx=50, pady=(10, 15))

        # Insights
        insights = self.generate_insights(self.transactions)

        for text in insights:
            Label(summary_frame, text=text, bg="black", fg="white",
                  font=("Arial", 17), anchor="w", justify="left",
                  wraplength=1100).pack(fill="x", padx=70, pady=8)

    # Function to generate insights from JSON
    def generate_insights(self, transactions):
        insights = []

        # Highest category spending
        category_totals = {}
        for t in transactions:
            cat = t["category"]
            category_totals[cat] = category_totals.get(cat, 0) + t["amount"]

        highest_category = max(category_totals, key=category_totals.get)
        insights.append(f"• Highest spending category: {highest_category} (£{category_totals[highest_category]})")

        # Most recent transaction
        last = transactions[-1]
        insights.append(f"• Your most recent transaction: £{last['amount']} on {last['merchant']} ({last['category']})")

        # Latest month spending
        latest_month = transactions[-1]["month"]
        month_total = sum(t["amount"] for t in transactions if t["month"] == latest_month)
        insights.append(f"• Total spending in {latest_month}: £{month_total}")

        # Food spending breakdown
        food_total = category_totals.get("Food", 0)
        insights.append(f"• You have spent £{food_total} on Food overall")

        return insights


#Start the Tkinter application loop
if __name__ == "__main__":
    root = Tk()
    app = DashboardApp(root)
    root.mainloop()
