import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk 
import mysql.connector

def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )

def submit_feedback():
    name = name_entry.get()
    reg_num = registration_entry.get()
    category = category_var.get()
    answers = [entry.get() for entry in question_entries]

    conn = connect_to_mysql()
    cursor = conn.cursor()

    sql = f"""INSERT INTO {category.lower()}_feedback 
              (name, registrationnumber, q1, q2, q3, q4, q5, q6, q7, q8)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    cursor.execute(sql, (name, reg_num, *answers))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Feedback Submitted", "Thank you for your feedback!")
    name_entry.delete(0, tk.END)
    registration_entry.delete(0, tk.END)
    for entry in question_entries:
        entry.delete(0, tk.END)
    toggle_questions_visibility(False)

def select_category(event):
    category = category_var.get()
    if category == "Administration":
        questions = [
            "Is administrative staff helpful and responsive?",
            "Are processes clear and transparent?",
            "Is student support adequate?",
            "Are facilities well-maintained?",
            "Are communication channels effective?",
            "Is the response time reasonable?",
            "Are policies fair and clearly stated?",
            "Any additional comments about the administration?"
        ]
    elif category == "Classroom":
        questions = [
            "Are classrooms well-equipped?",
            "Is the seating arrangement comfortable?",
            "Is there adequate lighting and ventilation?",
            "Are audio-visual aids functional?",
            "Is the teaching environment conducive?",
            "Are classroom facilities well-maintained?",
            "Are emergency exits accessible?",
            "Any additional comments about the classrooms?"
        ]
    elif category == "Hostel":
        questions = [
            "Is there any connectivity problem in the hostel?",
            "Are bathrooms and rooms cleaned regularly?",
            "Are the room furnishings in good condition?",
            "Is the maintenance staff responsive?",
            "Are quiet hours enforced?",
            "Is the hostel environment safe?",
            "Are there any noise issues?",
            "Any additional comments about the hostel?"
        ]
    elif category == "Library":
        questions = [
            "Is the library collection adequate?",
            "Are the seating arrangements comfortable?",
            "Is the library environment conducive for studying?",
            "Are digital resources accessible?",
            "Is the library staff helpful?",
            "Are quiet zones enforced?",
            "Are library hours convenient?",
            "Any additional comments about the library?"
        ]
    elif category == "Mess":
        questions = [
            "Is the food quality satisfactory?",
            "Is the mess area clean and hygienic?",
            "Are serving times convenient?",
            "Is the mess staff courteous?",
            "Are there adequate food choices?",
            "Is the seating arrangement comfortable?",
            "Are special dietary needs accommodated?",
            "Any additional comments about the mess?"
        ]
    elif category == "Sports Facilities":
        questions = [
            "Are sports facilities well-maintained?",
            "Is the equipment adequate and functional?",
            "Are facility hours convenient?",
            "Is the staff supportive?",
            "Are there enough facilities for different sports?",
            "Is there any issue with cleanliness?",
            "Are safety measures in place?",
            "Any additional comments about sports facilities?"
        ]

    for label, question in zip(question_labels, questions):
        label.config(text=question)
    toggle_questions_visibility(True)

def toggle_questions_visibility(visible):
    state = "normal" if visible else "hidden"
    for icon_label, lbl, entry in zip(icon_labels, question_labels, question_entries):
        icon_label.grid_remove() if not visible else icon_label.grid()
        lbl.grid_remove() if not visible else lbl.grid()
        entry.grid_remove() if not visible else entry.grid()

root = tk.Tk()
root.title("College Feedback System")
root.geometry("650x750")
root.config(bg="#eaeef7")



bg_image = Image.open("background.jpg")
bg_image = bg_image.resize((650, 750), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)



header_frame = tk.Frame(root, bg="#34495e")
header_frame.pack(fill=tk.X)
header_label = tk.Label(header_frame, text="College Feedback System", font=("Helvetica", 18, "bold"), fg="white", bg="#34495e")
header_label.pack(pady=15)



instructions = tk.Label(root, text="Please fill in your feedback details below:", font=("Helvetica", 12), bg="#eaeef7")
instructions.pack(pady=10)



form_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="solid", highlightthickness=1, highlightbackground="#d6eaf8")
form_frame.pack(pady=10, padx=20)



name_label = tk.Label(form_frame, text="Name:", font=("Helvetica", 10), bg="#ffffff")
name_label.grid(row=0, column=0, sticky="e", padx=10, pady=5)
name_entry = tk.Entry(form_frame, width=40)
name_entry.grid(row=0, column=1, padx=10, pady=5)


registration_label = tk.Label(form_frame, text="Registration Number:", font=("Helvetica", 10), bg="#ffffff")
registration_label.grid(row=1, column=0, sticky="e", padx=10, pady=5)
registration_entry = tk.Entry(form_frame, width=40)
registration_entry.grid(row=1, column=1, padx=10, pady=5)



category_label = tk.Label(form_frame, text="Feedback Category:", font=("Helvetica", 10), bg="#ffffff")
category_label.grid(row=2, column=0, sticky="e", padx=10, pady=5)
category_var = tk.StringVar()
category_menu = ttk.Combobox(form_frame, textvariable=category_var, values=["Administration", "Classroom", "Hostel", "Library", "Mess", "Sports Facilities"], width=37)
category_menu.grid(row=2, column=1, padx=10, pady=5)
category_menu.bind("<<ComboboxSelected>>", select_category)


icons = []
icon_labels = []
question_labels = []
question_entries = []
for i in range(8):
    icon = Image.open("question_icon.png")  
    icon = icon.resize((15, 15), Image.LANCZOS)
    icon_photo = ImageTk.PhotoImage(icon)
    icons.append(icon_photo)

    icon_label = tk.Label(form_frame, image=icon_photo, bg="#ffffff")
    icon_label.grid(row=3 + i, column=0, sticky="e", padx=5, pady=5)
    icon_labels.append(icon_label)

    lbl = tk.Label(form_frame, font=("Helvetica", 10), bg="#ffffff")
    lbl.grid(row=3 + i, column=1, sticky="w", padx=10, pady=5)
    entry = tk.Entry(form_frame, width=40)
    entry.grid(row=3 + i, column=2, padx=10, pady=5)

    question_labels.append(lbl)
    question_entries.append(entry)


toggle_questions_visibility(False)  



submit_button = tk.Button(root, text="Submit Feedback", command=submit_feedback, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
submit_button.pack(pady=20)

root.mainloop()
