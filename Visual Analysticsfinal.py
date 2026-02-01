from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json

#Class that controls the entire Visual Analytics screen layout using Tkinter
class VisualAnalyticsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visual Analytics")
        self.root.geometry("1300x780")
        self.root.config(bg="white")
        self.root.minsize(1300, 780)

        #Header section that includes the logo, navigation bar, and search bar for consistency across screens
        header_frame = Frame(self.root, bg="white", height=110)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        #Using GRID instead of PACK to fix alignment
        header_frame.columnconfigure(0, weight=0)

        # Logo on the left (resized to fit better into layout)
        try:
            logo_img = Image.open("logo copy 2.png")
            logo_img = logo_img.resize((90, 90))
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            Label(header_frame, image=self.logo_photo, bg="white").grid(row=0, column=0, padx=25, sticky="w")
        except:
            Label(header_frame, text="[LOGO]", bg="white", fg="black",
                  width=10, height=4, relief="groove").grid(row=0, column=0, padx=25)

        # Center frame for navigation and search bar
        center_frame = Frame(header_frame, bg="white")
        center_frame.grid(row=0, column=1, sticky="ew")

        # Navigation menu on the right – allows user to explore other screens
        nav_frame = Frame(center_frame, bg="white")
        nav_frame.pack(side="left", padx=(20, 10))
        nav_items = ["Dashboard", "Transactions", "Visual Analytics", "Budget", "Help"]
        for item in nav_items:
            Button(nav_frame, text=item, bg="white", fg="black",
                   font=("Arial", 13, "bold"), padx=10, pady=3,
                   relief="groove", bd=1).pack(side="left", padx=6)

        # Search bar
        search_frame = Frame(center_frame, bg="white")
        search_frame.pack(side="left", padx=(50, 0))
        self.search_entry = Entry(search_frame, width=35, relief="solid", font=("Arial", 11))
        self.search_entry.insert(0, "🔍  Search...")
        self.search_entry.pack(ipady=6)

        # Profile Section
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
       
        #Profile button
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
        self.profile_menu.add_command(label="My Account")
        self.profile_menu.add_command(label="Settings")
        self.profile_menu.add_separator()
        self.profile_menu.add_command(label="Logout")

        profile_button.bind("<Button-1>", show_profile_menu)


        #To update the geometric size
        self.root.update()

           
        # Load transaction data from JSON file
        with open("data.json", "r") as file:
            data = json.load(file)

        transactions = data["transactions"]

        #calling real-time notifcations
        self.show_notifications(transactions)

        #Calculate total
        category_totals = {}
        monthly_totals = {}

        for t in transactions:
            category = t["category"]
            month = t["month"]
            amount = t["amount"]
            category_totals[category] = category_totals.get(category, 0) + amount
            monthly_totals[month] = monthly_totals.get(month, 0) + amount

        #Main frame
        main_frame = Frame(self.root, bg="white")
        main_frame.pack(pady=20, padx=40)

        #Top frame to contain pie chart and insights
        top_frame = Frame(main_frame, bg="white")
        top_frame.pack(fill="x", pady=(10, 30))

        #Pie chart
        pie_frame = Frame(top_frame, bg="white")
        pie_frame.pack(side="left", padx=(40, 50))

        fig1 = Figure(figsize=(4, 4), dpi=100)
        ax1 = fig1.add_subplot(111)
        ax1.pie(category_totals.values(), labels=category_totals.keys(), autopct="%1.1f%%")
        ax1.set_title("Spending Breakdown")

        pie_canvas = FigureCanvasTkAgg(fig1, pie_frame)
        pie_canvas.draw()
        pie_canvas.get_tk_widget().pack()

        #Insight box
        insight_frame = Frame(top_frame, bg="white", bd=1, relief="solid", width=500, height=250)
        insight_frame.pack(side="left", padx=40)
        insight_frame.pack_propagate(False)

        Label(insight_frame, text="Spending Insight", bg="white",
              font=("Arial", 12, "bold")).pack(anchor="nw", pady=10, padx=10)

        insights = self.generate_insights(transactions)

        for text in insights:
            Label(insight_frame,
                  text=f"• {text}",
                  bg="white",
                  fg="black",
                  font=("Arial", 11),
                  wraplength=450,
                  anchor="w",
                  justify="left").pack(anchor="nw", padx=20, pady=5)

        #Bottom frame for bar chart and trends
        bottom_frame = Frame(main_frame, bg="white")
        bottom_frame.pack(fill="x", pady=(0, 20))

        # Bar chart
        bar_frame = Frame(bottom_frame, bg="white")
        bar_frame.pack(side="left", padx=(60, 40))

        fig2 = Figure(figsize=(4, 2.8), dpi=100)
        ax2 = fig2.add_subplot(111)
        months = ["Jan", "Feb", "March", "April", "May", "June"]
        totals = [monthly_totals[m] for m in months if m in monthly_totals]

        ax2.bar(months[:len(totals)], totals, color="#f7b2b0")
        ax2.set_facecolor("white")

        bar_canvas = FigureCanvasTkAgg(fig2, bar_frame)
        bar_canvas.draw()
        bar_canvas.get_tk_widget().pack()

        # Monthly trend text
        trends_frame = Frame(bottom_frame, bg="white")
        trends_frame.pack(side="left", padx=40, anchor="n")

        Label(trends_frame, text="Monthly Spending Trends",
              font=("Arial", 14, "italic"), bg="white", fg="black").pack(anchor="nw", pady=(10, 10))

        for line in [
            "Spending on housing remains high.",
            "Entertainment spending decreased this month.",
            "Food and transport stable overall.",
            "Overall savings trend upward."
        ]:
            Label(trends_frame, text=line, bg="white",
                  fg="black", font=("Arial", 11)).pack(anchor="w", pady=3)

    #real-time notification function
    def show_notifications(self, transactions):

        recent = transactions[-3:]

        messages = [f"New: £{t['amount']} spent on {t['category']}" for t in recent]
        notification_text = "\n".join(messages)

        self.notification_frame = Frame(self.root, bg="white")
        self.notification_frame.pack(fill="x", pady=(5, 5))

        self.notification_label = Label(
            self.notification_frame,
            text=notification_text,
            bg="#A91010",
            fg="white",
            font=("Arial", 12),
            padx=12,
            pady=6,
            anchor="w",
            justify="left"
        )
        self.notification_label.pack()

        #Auto remove after 5 seconds
        self.root.after(5000, self.notification_frame.destroy)

    #Insight function5
    def generate_insights(self, transactions):

        insights = []

        # Highest category spending
        category_totals = {}
        for t in transactions:
            category_totals[t["category"]] = category_totals.get(t["category"], 0) + t["amount"]

        highest = max(category_totals, key=category_totals.get)
        insights.append(f"Highest spending category: {highest} (£{category_totals[highest]})")

        # Most recent transaction
        last = transactions[-1]
        insights.append(f"Most recent: £{last['amount']} at {last['merchant']} ({last['category']})")

        # Spend in latest month
        latest_month = last["month"]
        month_total = sum(t["amount"] for t in transactions if t["month"] == latest_month)
        insights.append(f"Total spent in {latest_month}: £{month_total}")

        # Food total
        food_total = category_totals.get("Food", 0)
        insights.append(f"Total spent on Food: £{food_total}")

        return insights


#Start the Tkinter application loop
if __name__ == "__main__":
    root = Tk()
    app = VisualAnalyticsApp(root)
    root.mainloop()
