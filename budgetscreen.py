from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json

#Class that controls the entire Budget screen layout using Tkinter
class BudgetScreenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Screen")
        self.root.geometry("1300x780")
        self.root.config(bg="white")

        #Header section that includes the logo, navigation bar, and search bar for consistency across screens
        header_frame = Frame(self.root, bg="white", height=110)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        # Logo on the left (resized to fit better into layout)
        try:
            logo_img = Image.open("logo copy 2.png")
            logo_img = logo_img.resize((90, 90))
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            Label(header_frame, image=self.logo_photo, bg="white").grid(row=0, column=0, padx=25, sticky="w")
        except:
            Label(header_frame, text="[LOGO]", bg="white", fg="black",
                  width=10, height=4, relief="groove").grid(row=0, column=0, padx=25, sticky="w")

        # Centre frame for navigation and search bar
        center_frame = Frame(header_frame, bg="white")
        center_frame.grid(row=0, column=1, sticky="ew")

        nav_frame = Frame(center_frame, bg="white")
        nav_frame.pack(side="left", padx=(20, 10))
        for item in ["Dashboard", "Transactions", "Visual Analytics", "Budget", "Help"]:
            Button(nav_frame, text=item, bg="white", fg="black",
                   font=("Arial", 13, "bold"), padx=10, pady=3,
                   relief="groove", bd=1).pack(side="left", padx=6)

        search_frame = Frame(center_frame, bg="white")
        search_frame.pack(side="left", padx=(50, 0))
        self.search_entry = Entry(search_frame, width=35, relief="solid", font=("Arial", 11))
        self.search_entry.insert(0, "🔍  Search...")
        self.search_entry.pack(ipady=6)

        # Profile
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

        def show_profile_menu(event):
            x = event.widget.winfo_rootx()
            y = event.widget.winfo_rooty() + event.widget.winfo_height()
            self.profile_menu.tk_popup(x, y)

        profile_button = Button(profile_frame, text="Profile ▼", bg="#f2f2f2", fg="black",
                                font=("Arial", 10, "bold"), relief="groove", bd=1,
                                padx=15, pady=5)
        profile_button.pack(pady=(5, 0))

        self.profile_menu = Menu(self.root, tearoff=0, bg="white", fg="black", font=("Arial", 11))
        self.profile_menu.add_command(label="My Account")
        self.profile_menu.add_command(label="Settings")
        self.profile_menu.add_separator()
        self.profile_menu.add_command(label="Logout")
        profile_button.bind("<Button-1>", show_profile_menu)

        # Load transaction data from JSON file
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
            self.transactions = data.get("transactions", [])
            self.budgets = data.get("budgets", [])
        except:
            self.transactions = []
            self.budgets = []
            messagebox.showerror("Error", "Could not load data.json")

        #Main frame
        main_frame = Frame(self.root, bg="white")
        main_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # top row
        top_row = Frame(main_frame, bg="white")
        top_row.pack(fill="x", pady=(0, 20))

        # bottom row
        bottom_row = Frame(main_frame, bg="white")
        bottom_row.pack(fill="x")

        #Budget Input panel 
        input_frame = Frame(top_row, bg="black", bd=2, relief="solid", width=280, height=330)
        input_frame.pack(side="left", padx=(0, 40))
        input_frame.pack_propagate(False)

        Label(input_frame, text="Budget Input", font=("Arial", 16, "bold"),
              bg="black").pack(pady=(15, 10), anchor="w", padx=15)

        Label(input_frame, text="Budget Limit", bg="black",
              font=("Arial", 16)).pack(pady=(5, 2), padx=15, anchor="w")
        self.limit_entry = Entry(input_frame, width=24, relief="solid")
        self.limit_entry.pack(pady=(0, 12), padx=15)

        Label(input_frame, text="Category", bg="black",
              font=("Arial", 14)).pack(pady=(5, 2), padx=15, anchor="w")
        self.category_dropdown = ttk.Combobox(
            input_frame,
            values=["Food", "Shopping", "Transport", "Entertainment"],
            state="readonly",
            width=21
        )
        self.category_dropdown.pack(pady=(0, 18), padx=15)

        Button(input_frame, text="Save Budget", width=22,
               command=self.save_budget).pack(pady=4)
    
        Button(input_frame, text="Delete Budget", width=22,
               command=self.delete_budget).pack(pady=4)

        #Total Monthly Budget panel
        budget_frame = Frame(top_row, bg="", bd=2, relief="solid",
                             width=650, height=260)
        budget_frame.pack(side="left", padx=(0, 0))
        budget_frame.pack_propagate(False)

        Label(budget_frame, text="Total Monthly Budget",
              font=("Arial", 20, "bold"), bg="black").pack(anchor="nw",
                                                           padx=25, pady=(18, 5))

        # Calculate totals from JSON budgets + transactions
        self.total_budget = sum(b["limit"] for b in self.budgets) if self.budgets else 500
        self.spent_total = sum(t["amount"] for t in self.transactions)
        remaining = max(self.total_budget - self.spent_total, 0)

        Label(budget_frame, text="Remaining budget",
              font=("Arial", 13), bg="black").pack(anchor="nw",
                                                   padx=25, pady=(10, 2))

        #Bar showing how much is spent
        bar_canvas = Canvas(budget_frame, width=500, height=20,
                            bg="white", highlightthickness=0)
        bar_canvas.pack(padx=25, pady=6)

        if self.total_budget > 0:
            used_ratio = min(self.spent_total / self.total_budget, 1)
        else:
            used_ratio = 0

        #  Grey full bar
        bar_canvas.create_rectangle(0, 0, 500, 20, fill="#344BE1", outline="")
        # black used part
        bar_canvas.create_rectangle(0, 0, 500 * used_ratio, 20, fill="red", outline="")

        Label(budget_frame,
              text=f"Spent so far: £{self.spent_total:.2f}   |   Remaining: £{remaining:.2f}",
              font=("Arial", 12), bg="black").pack(anchor="nw",
                                                   padx=25, pady=(12, 0))

        #Category Breakdown panel
        category_frame = Frame(bottom_row, bg="white", bd=2, relief="solid",
                               width=650, height=260)
        category_frame.pack(side="left", padx=(320, 0), pady=(10, 0))  # push to centre-ish
        category_frame.pack_propagate(False)

        Label(category_frame, text="Category Breakdown",
              font=("Arial", 16, "bold"), bg="white").pack(anchor="nw",
                                                           padx=25, pady=(15, 10))

        #Build category totals from transactions
        category_totals = {}
        for t in self.transactions:
            cat = t["category"]
            category_totals[cat] = category_totals.get(cat, 0) + t["amount"]

        #Pie chart on left
        pie_frame = Frame(category_frame, bg="white")
        pie_frame.pack(side="left", padx=(30, 20), pady=5)

        fig = Figure(figsize=(2.8, 2.8), dpi=100)
        ax = fig.add_subplot(111)

        if category_totals:
            ax.pie(category_totals.values(), labels=category_totals.keys(),
                   autopct="%1.1f%%")
        else:
            ax.text(0.5, 0.5, "No data", ha="center", va="center")

        pie_canvas = FigureCanvasTkAgg(fig, pie_frame)
        pie_canvas.draw()
        pie_canvas.get_tk_widget().pack()

        #Simple text summary on right – like “£300/£500 used”
        summary_frame = Frame(category_frame, bg="white")
        summary_frame.pack(side="left", padx=10, pady=5, anchor="n")

        # example: show Food as first category if it exists
        if "Food" in category_totals:
            used_food = category_totals["Food"]
            # choose budget for Food if present
            food_limit = 0
            for b in self.budgets:
                if b["category"] == "Food":
                    food_limit = b["limit"]
                    break

            Label(summary_frame, text="Category", font=("Arial", 18, "bold"),
                  bg="black").pack(anchor="w")
            Label(summary_frame, text="Food", font=("Arial", 13),
                  bg="black").pack(anchor="w", pady=(0, 6))

            Label(summary_frame,
                  text=f"£{used_food:.0f} / £{food_limit or 500} used",
                  font=("Arial", 13), bg="black").pack(anchor="w")

        # if no food category, you could show a generic message
        else:
            Label(summary_frame, text="No Food category data yet.",
                  bg="black", font=("Arial", 11)).pack(anchor="w")

    #Budget functions

    def save_budget(self):
        """Save a new budget (simple prototype behaviour)."""
        try:
            limit = float(self.limit_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Budget limit must be a number.")
            return

        category = self.category_dropdown.get()
        if not category:
            messagebox.showerror("Error", "Please select a category.")
            return

        # add to in-memory list
        self.budgets.append({"category": category, "limit": limit})
        messagebox.showinfo("Saved", f"Budget for {category} saved.")

  
    def delete_budget(self):
        messagebox.showinfo("Delete Budget",
                            "Delete budget will be added in the next prototype.")


if __name__ == "__main__":
    root = Tk()
    app = BudgetScreenApp(root)
    root.mainloop()
