import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import json
import os
import random
import time  # Importing time module to measure execution time

class ToDoListManager:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("To-Do List Manager")
        self.parent.geometry("600x700")

        # Load Background Image
        self.bg_image = Image.open("C:\\Users\\rainr\\OneDrive\\Desktop\\Assignment\\A_soft_pink_gradient_background_with_elegant_abstr.png")  # Make sure the file exists
        self.bg_image = self.bg_image.resize((600, 700), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        self.canvas = tk.Canvas(self.parent, width=600, height=700)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Frame to hold widgets
        self.frame = tk.Frame(self.parent, bg="white", bd=2, relief="groove")
        self.frame.place(x=50, y=50, width=500, height=600)

        self.task_list = []
        self.contacts = []
        self.points = 0
        self.completed_tasks = 0

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        header_label = ttk.Label(self.frame, text="To-Do List Manager", font=("Arial", 18, "bold"), background="white", foreground="#FF69B4")
        header_label.pack(pady=10)

        self.task_entry = ttk.Entry(self.frame, width=40)
        self.task_entry.pack(pady=10)
        
        self.priority_var = tk.StringVar()
        self.priority_combobox = ttk.Combobox(self.frame, textvariable=self.priority_var, values=["High", "Medium", "Low"], state="readonly", width=18)
        self.priority_combobox.pack(pady=5)
        self.priority_combobox.current(1)

        self.add_task_button = ttk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=5)

        self.task_listbox = tk.Listbox(self.frame, selectmode=tk.SINGLE, width=50, height=10)
        self.task_listbox.pack(pady=10)

        self.complete_task_button = ttk.Button(self.frame, text="Complete Task", command=self.complete_task)
        self.complete_task_button.pack(pady=5)

        self.delete_task_button = ttk.Button(self.frame, text="Delete Task", command=self.delete_task)
        self.delete_task_button.pack(pady=5)

        self.view_analytics_button = ttk.Button(self.frame, text="View Analytics", command=self.view_analytics)
        self.view_analytics_button.pack(pady=5)

        self.points_label = ttk.Label(self.frame, text=f"Points: {self.points}", background="white")
        self.points_label.pack(pady=5)

        self.reward_button = ttk.Button(self.frame, text="Get Motivated!", command=self.show_reward, state=tk.DISABLED)
        self.reward_button.pack(pady=5)

        self.contacts_button = ttk.Button(self.frame, text="Manage Contacts", command=self.open_contacts_window)
        self.contacts_button.pack(pady=5)

    def add_task(self):
        start_time = time.time()  # Start the timer
        task = self.task_entry.get()
        priority = self.priority_var.get()
        if task:
            self.task_list.append((task, priority))
            self.task_listbox.insert(tk.END, f"{task} ({priority} Priority)")
            self.task_entry.delete(0, tk.END)
            self.save_data()
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"Time taken to add task: {elapsed_time:.4f} seconds")  # Print the elapsed time

    def complete_task(self):
        start_time = time.time()  # Start the timer
        selected = self.task_listbox.curselection()
        if selected:
            self.task_listbox.delete(selected)
            self.completed_tasks += 1
            self.points += 10
            self.update_points()
            self.save_data()
        else:
            messagebox.showwarning("Warning", "Please select a task!")
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"Time taken to complete task: {elapsed_time:.4f} seconds")  # Print the elapsed time

    def delete_task(self):
        start_time = time.time()  # Start the timer
        selected = self.task_listbox.curselection()
        if selected:
            self.task_listbox.delete(selected)
            del self.task_list[selected[0]]
            self.save_data()
        else:
            messagebox.showwarning("Warning", "Please select a task to delete!")
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"Time taken to delete task: {elapsed_time:.4f} seconds")  # Print the elapsed time

    def update_points(self):
        self.points_label.config(text=f"Points: {self.points}")
        if self.points >= 10:
            self.reward_button.config(state=tk.NORMAL)
        else:
            self.reward_button.config(state=tk.DISABLED)

    def show_reward(self):
        rewards = [
            "Keep pushing forward!", "Believe in yourself!", "Success comes from effort!"
        ]
        messagebox.showinfo("Motivation", random.choice(rewards))
        self.points -= 10
        self.update_points()

    def view_analytics(self):
        tasks_added = len(self.task_list)
        message = f"Tasks Added: {tasks_added}\nTasks Completed: {self.completed_tasks}\nPoints Earned: {self.points}"
        messagebox.showinfo("Analytics", message)

    def open_contacts_window(self):
        contacts_window = tk.Toplevel(self.parent)
        contacts_window.title("Contact Manager")
        contacts_window.geometry("500x500")
        contacts_window.configure(bg="white")

        # Labels and Entry fields in grid layout
        ttk.Label(contacts_window, text="Name:").grid(row=0, column=0, pady=5, padx=10, sticky="e")
        self.contact_name_entry = ttk.Entry(contacts_window, width=30)
        self.contact_name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(contacts_window, text="Phone Number:").grid(row=1, column=0, pady=5, padx=10, sticky="e")
        self.contact_phone_entry = ttk.Entry(contacts_window, width=30)
        self.contact_phone_entry.grid(row=1, column=1, pady=5)

        ttk.Label(contacts_window, text="Email:").grid(row=2, column=0, pady=5, padx=10, sticky="e")
        self.contact_email_entry = ttk.Entry(contacts_window, width=30)
        self.contact_email_entry.grid(row=2, column=1, pady=5)

        ttk.Label(contacts_window, text="City:").grid(row=3, column=0, pady=5, padx=10, sticky="e")
        self.contact_city_entry = ttk.Entry(contacts_window, width=30)
        self.contact_city_entry.grid(row=3, column=1, pady=5)

        ttk.Label(contacts_window, text="Country:").grid(row=4, column=0, pady=5, padx=10, sticky="e")
        self.contact_country_entry = ttk.Entry(contacts_window, width=30)
        self.contact_country_entry.grid(row=4, column=1, pady=5)

        ttk.Button(contacts_window, text="Add Contact", command=self.add_contact).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(contacts_window, text="View Contacts", command=self.view_all_contacts).grid(row=6, column=0, columnspan=2, pady=5)
        ttk.Button(contacts_window, text="Search Contact", command=self.search_contact).grid(row=7, column=0, columnspan=2, pady=5)
        ttk.Button(contacts_window, text="Delete Contact", command=self.delete_contact).grid(row=8, column=0, columnspan=2, pady=5)

    def add_contact(self):
        start_time = time.time()  # Start the timer
        name = self.contact_name_entry.get()
        phone = self.contact_phone_entry.get()
        email = self.contact_email_entry.get()
        city = self.contact_city_entry.get()
        country = self.contact_country_entry.get()
        if name and email:
            self.contacts.append({"name": name, "phone": phone, "email": email, "city": city, "country": country})
            messagebox.showinfo("Success", "Contact added!")
            self.save_data()
        else:
            messagebox.showwarning("Warning", "Enter name and email!")
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"Time taken to add contact: {elapsed_time:.4f} seconds")  # Print the elapsed time

    def view_all_contacts(self):
        start_time = time.time()  # Start the timer
        contacts_info = "\n".join([f"{c['name']} - {c['phone']} - {c['email']} - {c['city']} - {c['country']}" for c in self.contacts])
        messagebox.showinfo("Contacts", contacts_info if contacts_info else "No contacts yet!")
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"Time taken to view all contacts: {elapsed_time:.4f} seconds")  # Print the elapsed time

    def search_contact(self):
        start_time = time.time()  # Start the timer
        name = self.contact_name_entry.get()
        found_contacts = [c for c in self.contacts if name.lower() in c['name'].lower()]
        if found_contacts:
            contacts_info = "\n".join([f"{c['name']} - {c['phone']} - {c['email']} - {c['city']} - {c['country']}" for c in found_contacts])
            messagebox.showinfo("Search Results", contacts_info)
        else:
            messagebox.showinfo("Search Results", "No contacts found.")
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"Time taken to search contact: {elapsed_time:.4f} seconds")  # Print the elapsed time

    def delete_contact(self):
        start_time = time.time()  # Start the timer
        name = self.contact_name_entry.get()
        self.contacts = [c for c in self.contacts if c['name'].lower() != name.lower()]
        messagebox.showinfo("Success", "Contact deleted!")
        self.save_data()
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"Time taken to delete contact: {elapsed_time:.4f} seconds")  # Print the elapsed time

    def save_data(self):
        start_time = time.time()  # Start the timer
        data = {"tasks": self.task_list, "contacts": self.contacts, "points": self.points, "completed_tasks": self.completed_tasks}
        with open("data.json", "w") as f:
            json.dump(data, f)  # O(n) due to the need to serialize the entire task list
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"Time taken to save data: {elapsed_time:.4f} seconds")  # Print the elapsed time

    def load_data(self):
        start_time = time.time()  # Start the timer
        if os.path.exists("data.json"):
            with open("data.json", "r") as f:
                data = json.load(f)  # O(n) since it loads the entire file
                self.task_list = data.get("tasks", [])
                self.contacts = data.get("contacts", [])
                self.points = data.get("points", 0)
                self.completed_tasks = data.get("completed_tasks", 0)
                for task, priority in self.task_list:
                    self.task_listbox.insert(tk.END, f"{task} ({priority} Priority)")  # O(n) for inserting tasks into the listbox
        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"Time taken to load data: {elapsed_time:.4f} seconds")  # Print the elapsed time

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListManager(root)
    root.mainloop()
