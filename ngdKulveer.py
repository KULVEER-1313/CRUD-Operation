import tkinter as tk
from tkinter import messagebox, scrolledtext, Toplevel
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["TransportDB"]
collection = db["vehicles"]

# Window
root = tk.Tk()
root.title("Vehicle Registry - Kulveer Singh")
root.geometry("650x450")

# Title
title = tk.Label(root, text="497 - Kulveer Singh | Vehicle Registry (MongoDB + Tkinter)", 
                 font=("Helvetica", 15, "bold"), fg="darkblue")
title.pack(pady=15)

# Frame for form
form_frame = tk.Frame(root)
form_frame.pack(pady=10)

# Labels & Entry fields
tk.Label(form_frame, text="Registration No:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
reg_entry = tk.Entry(form_frame, width=35)
reg_entry.grid(row=0, column=1, pady=5)

tk.Label(form_frame, text="Owner Name:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
owner_entry = tk.Entry(form_frame, width=35)
owner_entry.grid(row=1, column=1, pady=5)

tk.Label(form_frame, text="Vehicle Type:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
type_entry = tk.Entry(form_frame, width=35)
type_entry.grid(row=2, column=1, pady=5)

tk.Label(form_frame, text="City:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
city_entry = tk.Entry(form_frame, width=35)
city_entry.grid(row=3, column=1, pady=5)

# ---------------- Insert ----------------
def insert():
    reg_no = reg_entry.get().strip()
    owner = owner_entry.get().strip()
    v_type = type_entry.get().strip()
    city = city_entry.get().strip()

    if not (reg_no and owner and v_type and city):
        messagebox.showwarning("Missing Data", "Please fill all fields.")
        return

    try:
        collection.insert_one({"reg_no": reg_no, "owner": owner, "type": v_type, "city": city})
        messagebox.showinfo("Success", "Vehicle added successfully!")
        reg_entry.delete(0, tk.END)
        owner_entry.delete(0, tk.END)
        type_entry.delete(0, tk.END)
        city_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Insert failed: {e}")

# ---------------- Read ----------------
def read():
    try:
        documents = collection.find()
        result_text.delete(1.0, tk.END)
        for doc in documents:
            result_text.insert(tk.END, f"Reg No: {doc['reg_no']}, Owner: {doc['owner']}, Type: {doc['type']}, City: {doc['city']}\n")
    except:
        messagebox.showerror("Error", "Failed to fetch records")

# ---------------- Update ----------------
def update():
    win = Toplevel(root)
    win.title("Update Vehicle")
    win.geometry("400x250")

    tk.Label(win, text="Enter Owner Name to Update:").pack(pady=5)
    old_owner_entry = tk.Entry(win, width=30)
    old_owner_entry.pack()

    tk.Label(win, text="New Vehicle Type:").pack(pady=5)
    new_type_entry = tk.Entry(win, width=30)
    new_type_entry.pack()

    tk.Label(win, text="New City:").pack(pady=5)
    new_city_entry = tk.Entry(win, width=30)
    new_city_entry.pack()

    def confirm_update():
        old_owner = old_owner_entry.get().strip()
        new_type = new_type_entry.get().strip()
        new_city = new_city_entry.get().strip()

        if not (old_owner and new_type and new_city):
            messagebox.showwarning("Warning", "All fields are required!")
            return

        result = collection.update_one({"owner": old_owner}, {"$set": {"type": new_type, "city": new_city}})
        if result.modified_count > 0:
            messagebox.showinfo("Success", "Vehicle updated successfully!")
            win.destroy()
        else:
            messagebox.showinfo("Not Found", "No matching vehicle found.")

    tk.Button(win, text="Update Now", command=confirm_update).pack(pady=15)

# ---------------- Delete ----------------
def delete():
    win = Toplevel(root)
    win.title("Delete Vehicle")
    win.geometry("300x200")

    tk.Label(win, text="Enter Registration No to Delete:").pack(pady=10)
    del_reg_entry = tk.Entry(win, width=30)
    del_reg_entry.pack()

    def confirm_delete():
        del_reg = del_reg_entry.get().strip()
        if not del_reg:
            messagebox.showwarning("Warning", "Registration No is required!")
            return

        result = collection.delete_one({"reg_no": del_reg})
        if result.deleted_count > 0:
            messagebox.showinfo("Success", "Vehicle deleted successfully!")
            win.destroy()
        else:
            messagebox.showinfo("Not Found", "No vehicle found with given Registration No.")

    tk.Button(win, text="Delete Now", command=confirm_delete).pack(pady=15)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=15)

tk.Button(btn_frame, text="Insert", command=insert, width=12, bg="lightgreen").grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Show Vehicles", command=read, width=12, bg="lightblue").grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Update", command=update, width=12, bg="orange").grid(row=0, column=2, padx=10)
tk.Button(btn_frame, text="Delete", command=delete, width=12, bg="red").grid(row=0, column=3, padx=10)

# Result Text Area
result_text = scrolledtext.ScrolledText(root, width=75, height=8)
result_text.pack(pady=10)

root.mainloop()
