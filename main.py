import tkinter as tk
from tkinter import messagebox
from models import Customer, FoodOrder, CashPayment, CardPayment
from views import AppView, HoverButton, BTN_MENU, BTN_MENU_HOVER, BTN_DANGER, BTN_DANGER_HOVER

class AppController:
    def __init__(self, view):
        self.view = view
        self.current_order = FoodOrder() 
        self.all_orders = []

        # Populate UI Menu with modern HoverButtons
        for item_name, price in FoodOrder.MENU.items():
            btn = HoverButton(
                self.view.menu_frame, 
                bg_color=BTN_MENU, 
                hover_color=BTN_MENU_HOVER,
                text=f"{item_name}  —  ₱{price:.2f}", 
                fg="#0F172A", 
                font=("Segoe UI", 10, "bold"),
                command=lambda name=item_name: self.add_to_cart(name)
            )
            btn.pack(fill=tk.X, pady=4, ipady=4)

        self.view.btn_checkout.config(command=self.prompt_checkout)
        self.view.btn_verify.config(command=self.verify_payment)
        self.view.btn_update_status.config(command=self.open_status_manager)
        
        self.view.order_list.bind("<Double-1>", self.show_receipt_history)

        self.timer_loop()

    def add_to_cart(self, item_name):
        self.current_order.add_item(item_name)
        self.update_cart_ui()

    def remove_from_cart(self, item_name):
        self.current_order.remove_item(item_name)
        self.update_cart_ui()

    def update_cart_ui(self):
        for widget in self.view.cart_frame.winfo_children():
            widget.destroy()
            
        for item, qty in self.current_order._items.items():
            row = tk.Frame(self.view.cart_frame, bg="#FFFFFF")
            row.pack(fill=tk.X, pady=2, padx=10)
            
            lbl = tk.Label(row, text=f"{item} ({qty})", bg="#FFFFFF", fg="#0F172A", font=("Segoe UI", 10, "bold"))
            lbl.pack(side=tk.LEFT, pady=5)
            
            btn_minus = HoverButton(row, bg_color=BTN_DANGER, hover_color=BTN_DANGER_HOVER, 
                                    text="—", fg="white", font=("Segoe UI", 8, "bold"), width=3,
                                    command=lambda i=item: self.remove_from_cart(i))
            btn_minus.pack(side=tk.RIGHT)

        self.view.lbl_total.config(text=f"₱{self.current_order.total:.2f}")

    def prompt_checkout(self):
        if not self.current_order._items: 
            messagebox.showwarning("Empty Cart", "Please add items to your cart first.")
            return

        cust_name = self.view.entry_name.get().strip()
        if not cust_name:
            messagebox.showwarning("Missing Info", "Please enter a customer name.")
            return

        self.view.open_payment_prompt(self.process_checkout)

    def process_checkout(self, payment_type):
        if payment_type == "Cash":
            payment_method = CashPayment()
        else:
            payment_method = CardPayment()

        cust_name = self.view.entry_name.get().strip()

        self.current_order.customer = Customer(cust_name, "Address TBD")
        self.current_order.payment_method = payment_method
        self.current_order.status = "Pending Verification"
        
        self.all_orders.append(self.current_order)

        messagebox.showinfo("Order Submitted", "Order sent to Admin. Awaiting payment verification.")
        self.refresh_admin()

        self.current_order = FoodOrder()
        self.update_cart_ui()
        self.view.entry_name.delete(0, tk.END)

    def verify_payment(self):
        selection = self.view.order_list.curselection()
        if selection:
            idx = selection[0]
            order = self.all_orders[idx]
            
            if order.status == "Pending Verification":
                item_list = "\n".join(f"- {item} ({qty}) - ₱{FoodOrder.MENU[item] * qty:.2f}" 
                                      for item, qty in order._items.items())
                
                receipt_text = (
                    f"Receipt for {order.customer.name}\n"
                    f"------------------------\n"
                    f"{item_list}\n"
                    f"------------------------\n"
                    f"Total: ₱{order.total:.2f}\n"
                    f"{order.payment_method.process(order.total)}"
                )
                order.receipt = receipt_text
                
                self.change_status(order, "Preparing")
                messagebox.showinfo("Payment Approved", f"Payment verified!\n\n{order.receipt}")
            else:
                messagebox.showinfo("Status", f"Order is already past verification (Current Status: {order.status}).")

    def show_receipt_history(self, event):
        selection = self.view.order_list.curselection()
        if selection:
            idx = selection[0]
            order = self.all_orders[idx]
            if order.receipt:
                messagebox.showinfo(f"Receipt - Order {idx+1}", order.receipt)
            else:
                messagebox.showinfo("Receipt Not Available", "Payment has not been verified yet.")

    def open_status_manager(self):
        selection = self.view.order_list.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an order to update.")
            return
            
        idx = selection[0]
        order = self.all_orders[idx]
        
        if order.status == "Pending Verification":
            messagebox.showwarning("Action Denied", "You must verify the payment before updating delivery status!")
            return
            
        self.view.open_status_window(order.status, lambda new_status: self.change_status(order, new_status))

    def change_status(self, order, new_status):
        order.status = new_status
        if new_status == "Preparing":
            order.time_left = 300       
        elif new_status == "Ready for pickup":
            order.time_left = 300       
        elif new_status == "On its way":
            order.time_left = 900       
        else:
            order.time_left = 0         
            
        self.refresh_admin()

    def timer_loop(self):
        needs_refresh = False
        for order in self.all_orders:
            if order.time_left > 0:
                order.time_left -= 1
                needs_refresh = True
                
                if order.time_left == 0:
                    if order.status == "Preparing":
                        self.change_status(order, "Ready for pickup")
                    elif order.status == "Ready for pickup":
                        self.change_status(order, "On its way")
                    elif order.status == "On its way":
                        self.change_status(order, "Delivered")
                        
        if needs_refresh:
            self.refresh_admin()
            
        self.view.root.after(1000, self.timer_loop)

    def refresh_admin(self):
        selection = self.view.order_list.curselection()
        self.view.order_list.delete(0, tk.END)
        
        for i, order in enumerate(self.all_orders):
            timer_str = ""
            if order.time_left > 0:
                mins, secs = divmod(order.time_left, 60)
                timer_str = f" [{mins:02d}:{secs:02d}]"
                
            display_text = f"Ord {i+1} | {order.customer.name} | {order.status}{timer_str} | ₱{order.total:.2f}"
            self.view.order_list.insert(tk.END, display_text)
            
        if selection:
            self.view.order_list.selection_set(selection[0])

if __name__ == "__main__":
    root = tk.Tk()
    app_view = AppView(root)
    controller = AppController(app_view)
    root.mainloop()