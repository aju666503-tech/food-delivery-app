import tkinter as tk
from tkinter import messagebox
from models import Customer, FoodOrder, CashPayment, CardPayment
from views import AppView

class AppController:
    def __init__(self, view):
        self.view = view
        self.current_order = FoodOrder() # Start with no customer
        self.all_orders = []

        # Populate UI Menu from Model
        for item, price in FoodOrder.MENU.items():
            self.view.menu_list.insert(tk.END, f"{item} - ₱{price:.2f}")

        # Bind UI Buttons to Controller Methods
        self.view.menu_list.bind("<Double-1>", self.add_to_cart)
        self.view.btn_cash.config(command=lambda: self.checkout(CashPayment()))
        self.view.btn_card.config(command=lambda: self.checkout(CardPayment()))
        self.view.btn_dispatch.config(command=self.mark_delivered)

    def add_to_cart(self, event):
        selection = self.view.menu_list.curselection()
        if selection:
            item_name = self.view.menu_list.get(selection[0]).split(" - ")[0]
            self.current_order.add_item(item_name)
            self.view.lbl_total.config(text=f"₱{self.current_order.total:.2f}")

    def checkout(self, payment_method):
        """Demonstrates Polymorphism and registers a new Customer per order."""
        if not self.current_order._items: 
            return

        # NEW: Validate and create Customer from UI input
        cust_name = self.view.entry_name.get().strip()
        if not cust_name:
            messagebox.showwarning("Missing Info", "Please enter a customer name.")
            return

        # Assign dynamic customer to the order
        self.current_order.customer = Customer(cust_name, "Address TBD")
        
        # Process Payment
        receipt = payment_method.process(self.current_order.total)
        self.current_order.status = "Preparing"
        self.all_orders.append(self.current_order)

        messagebox.showinfo("Payment Success", receipt)
        self.refresh_admin()

        # Reset Cart and Input Field for the next order
        self.current_order = FoodOrder()
        self.view.lbl_total.config(text="₱0.00")
        self.view.entry_name.delete(0, tk.END) # Clears the name box

    def refresh_admin(self):
        """Updates the Admin Delivery Tracking board."""
        self.view.order_list.delete(0, tk.END)
        for i, order in enumerate(self.all_orders):
            self.view.order_list.insert(tk.END, f"Ord {i+1} | {order.customer.name} | {order.status}")

    def mark_delivered(self):
        """Admin action to update order status."""
        selection = self.view.order_list.curselection()
        if selection:
            idx = selection[0]
            self.all_orders[idx].status = "Delivered"
            self.refresh_admin()

if __name__ == "__main__":
    root = tk.Tk()
    app_view = AppView(root)
    controller = AppController(app_view)
    root.mainloop()