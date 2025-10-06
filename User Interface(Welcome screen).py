from tkinter import *
from PIL import ImageTk, Image

#configuration
myApp=Tk()
myApp.title("Welcome screen")
myApp.geometry("1000x10000")
myApp.config(background="white")

#image
image=PhotoImage(file="logo copy 2.png")
image_label= Label(myApp, image=image)
image_label.pack(side="left",anchor="n",padx=20,pady=20)

#Login Button
def on_button_click():
	messagebox.showinfo("Button Clicked", "Login")

button=Button(myApp,text="Login",bg="white",fg="black", padx=10, pady=10)
button.pack(pady=10, side="right",padx=10)

#Check box: "Remember me!"
def show_selection():
	if checkbox_var.get()==1:
	   messagebox.showinfo("Selection", "Remember Me!")
	else:
		messagebox.showinfo("Selection", "Please tick checkbox!")

#object to hold state of checkbox
checkbox_var=IntVar()

checkbox=ttk.Checkbutton(myApp,text="I agree to the terms and conditions", variable= checkbox_var, onvalue=1, offvalue=0)
check_button=Button(myApp, text="Submit", command= show_selection)
check_button.pack(pady=10)
	

myApp.mainloop()
