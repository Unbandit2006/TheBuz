import tkinter as tk
from tkinter import ttk
from tkinter import font

global class_header_text
class_header_text = "Class Name"


def redraw(e):
  user_selection = str(
    class_treeview.item(class_treeview.focus()).get("values")[0])
  class_header_text = user_selection
  class_header.config(text=class_header_text)

  if user_selection == "Spanish 3 1 of 2":
    detail_treeview = ttk.Treeview(right_frame,
                                   columns=("Type", "Heading", "Grades",
                                            "Notes"),
                                   show="headings",
                                   height=100,
                                   padding=20)
    detail_treeview.heading("Type", text="Type")
    detail_treeview.heading("Heading", text="Name")
    detail_treeview.heading("Grades", text="Grade")
    detail_treeview.heading("Notes", text="Notes")

    detail_treeview.insert("",
                           tk.END,
                           values=("Material", "Preterit Tense Flashcards",
                                   "None", "Study This"))
    detail_treeview.insert("",
                           tk.END,
                           values=("Assessment", "Present Tense Test",
                                   "58/100", "None"))
    detail_treeview.insert("",
                           tk.END,
                           values=("Announcement", "Test Tomorrow", "None",
                                   "You better study"))
    detail_treeview.insert("",
                           tk.END,
                           values=("Assignment", "Present Tense Review HW",
                                   "90/100", "Nice Job."))

    detail_treeview.pack(fill="both", expand=True)


root = tk.Tk()
# root.attributes("-fullscreen", True)
root.state("zoomed")
root.config(background="#0E3659")

big_font = tk.font.Font(family="Arial", size=26, weight="bold")

root_style = ttk.Style()
root_style.configure("Treeview",
                     background="#D4E8FF",
                     fieldbackground="#D4E8FF")

left_frame = tk.Frame(root, background="#165081", width=500, height=500)

class_treeview = ttk.Treeview(left_frame,
                              columns="class",
                              show="headings",
                              height=100,
                              padding=20)
class_treeview.heading("class", text="Classes")
class_treeview.insert("", tk.END, values=("English 3 1 of 2", ))
class_treeview.insert("", tk.END, values=("AP Calc. 1 of 2", ))
class_treeview.insert("", tk.END, values=("Calc. Implementation 1 of 2", ))
class_treeview.insert("", tk.END, values=("Spanish 3 1 of 2", ))
class_treeview.insert("", tk.END, values=("Weight Training 1 of 2", ))
class_treeview.insert("", tk.END, values=("AP Comp. Sci. 3 1 of 2", ))
class_treeview.insert("", tk.END, values=("AP World History 1 of 2", ))
class_treeview.pack()
class_treeview.bind("<<TreeviewSelect>>", redraw)

left_frame.pack(side=tk.LEFT)

right_frame = tk.Frame(root, background="#165081", width=500, height=500)

class_header = tk.Label(right_frame,
                        font=big_font,
                        foreground="#FFFFFF",
                        background="#165081",
                        text="Class Name")
class_header.pack(side=tk.TOP)
right_frame.pack(side=tk.RIGHT, fill="both", expand=True)

root.mainloop()
