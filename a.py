import tkinter as tk
from tkinter import messagebox
import sqlite3

class CarRentalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Rental System")
        
        # Initialize database
        self.init_db()
        
        # Car selection
        self.car_label = tk.Label(root, text="Select a Car:")
        self.car_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.cars = ["Fortuner - ₹12000/day", "Lexus - ₹30000/day", "Endeavour - ₹20000/day", "Urus - ₹34000/day","Swift - ₹6000/day"]
        self.car_var = tk.StringVar(value=self.cars[0])
        self.car_menu = tk.OptionMenu(root, self.car_var, *self.cars)
        self.car_menu.grid(row=0, column=1, padx=10, pady=10)
        
        # Customer name
        self.name_label = tk.Label(root, text="Customer Name:")
        self.name_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Rental days
        self.days_label = tk.Label(root, text="Number of Days:")
        self.days_label.grid(row=2, column=0, padx=10, pady=10)
        
        self.days_entry = tk.Entry(root)
        self.days_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Calculate button
        self.calc_button = tk.Button(root, text="Calculate Cost", command=self.calculate_cost)
        self.calc_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Total cost
        self.cost_label = tk.Label(root, text="Total Cost: ₹0")
        self.cost_label.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Return car button
        self.return_button = tk.Button(root, text="Return Car", command=self.return_car)
        self.return_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Rental Records
        self.records_label = tk.Label(root, text="Rental Records")
        self.records_label.grid(row=6, column=0, columnspan=2, pady=10)
        
        self.records_text = tk.Text(root, height=10, width=50)
        self.records_text.grid(row=7, column=0, columnspan=2, pady=10)
        self.load_records()

    def init_db(self):
        self.conn = sqlite3.connect('car_rental.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS rentals (
                id INTEGER PRIMARY KEY,
                car TEXT,
                name TEXT,
                days INTEGER,
                cost INTEGER
            )
        ''')
        self.conn.commit()

    def calculate_cost(self):
        car = self.car_var.get()
        name = self.name_entry.get()
        days = self.days_entry.get()
        
        if not name or not days:
            messagebox.showerror("Input Error", "Please enter all the required fields.")
            return
        
        try:
            days = int(days)
            if days <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number of days.")
            return
        
        daily_cost = int(car.split('- ₹')[1].split('/')[0])
        total_cost = daily_cost * days
        self.cost_label.config(text=f"Total Cost: ₹{total_cost}")

        self.save_rental(car, name, days, total_cost)
        self.load_records()

    def save_rental(self, car, name, days, cost):
        self.cursor.execute('''
            INSERT INTO rentals (car, name, days, cost)
            VALUES (?, ?, ?, ?)
        ''', (car, name, days, cost))
        self.conn.commit()

    def load_records(self):
        self.records_text.delete(1.0, tk.END)
        self.cursor.execute('SELECT * FROM rentals')
        rentals = self.cursor.fetchall()
        for rental in rentals:
            self.records_text.insert(tk.END, f"ID: {rental[0]}, Car: {rental[1]}, Name: {rental[2]}, Days: {rental[3]}, Cost: ₹{rental[4]}\n")

    def return_car(self):
        try:
            record_id = int(self.records_text.get(tk.SEL_FIRST, tk.SEL_LAST).split(",")[0].split(":")[1].strip())
            self.cursor.execute('DELETE FROM rentals WHERE id = ?', (record_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Car returned successfully.")
            self.load_records()
        except (tk.TclError, IndexError, ValueError):
            messagebox.showerror("Selection Error", "Please select a valid rental record to return.")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = CarRentalApp(root)
    root.configure(background="light blue")
    root.mainloop()
