import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
from main import Menu, MenuItem, Customer, Order, CreditCardPayment, CashOnDelivery, Delivery

class FoodDeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QuickBite - Food Delivery System")
        self.root.geometry("800x680")
        self.root.config(bg="#F4F6F9")

        self.menu = Menu()
        self.setup_initial_data()
        
        # Default placeholder customer before login/setup
        self.customer = Customer("C1", "Guest User", "guest@example.com", "General Trias, Cavite", "09123456789")
        self.current_order = Order("ORD1001", self.customer)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.bg_color = "#F4F6F9"
        self.card_bg = "#FFFFFF"
        self.primary_color = "#2C3E50"
        self.accent_color = "#27AE60"
        self.button_blue = "#3498DB"

        self.create_widgets()
        
        # Prompt user to input information on startup
        self.root.after(100, self.open_customer_setup_dialog)

    def setup_initial_data(self):
        self.menu.add_item(MenuItem("M1", "Cheeseburger", 150.00, "Fast Food"))
        self.menu.add_item(MenuItem("M2", "Matcha Latte", 180.00, "Beverage"))
        self.menu.add_item(MenuItem("M3", "Fries", 80.00, "Fast Food"))
        self.menu.add_item(MenuItem("M4", "Chicken Wings", 220.00, "Fast Food"))

    def create_widgets(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=75)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="QuickBite Delivery System", fg="white", bg=self.primary_color, font=("Segoe UI", 16, "bold"))
        title_label.pack(side=tk.LEFT, padx=20, pady=20)

        # Right side header container for user info and edit button
        header_right = tk.Frame(header_frame, bg=self.primary_color)
        header_right.pack(side=tk.RIGHT, padx=20, pady=15)

        self.user_info_label = tk.Label(header_right, text=f"👤 {self.customer.name} | 📞 {self.customer.contact_number} | 📍 {self.customer.address}", fg="#BDC3C7", bg=self.primary_color, font=("Segoe UI", 9))
        self.user_info_label.pack(side=tk.TOP, anchor="e", pady=(0, 2))

        edit_profile_btn = tk.Button(header_right, text="Edit Profile / Address", bg="#34495E", fg="white", font=("Segoe UI", 8, "bold"), relief=tk.FLAT, cursor="hand2", command=self.open_customer_setup_dialog)
        edit_profile_btn.pack(side=tk.TOP, anchor="e")

        # Main Content Layout
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        top_section = tk.Frame(main_container, bg=self.bg_color)
        top_section.pack(fill=tk.BOTH, expand=True)

        # Left Card: Menu Selection
        left_card = tk.Frame(top_section, bg=self.card_bg, highlightbackground="#DCDDE1", highlightthickness=1)
        left_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tk.Label(left_card, text="Available Menu", bg=self.card_bg, fg=self.primary_color, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=15, pady=(15, 10))

        menu_frame = tk.Frame(left_card, bg=self.card_bg)
        menu_frame.pack(fill=tk.BOTH, expand=True, padx=15)

        self.menu_listbox = tk.Listbox(menu_frame, font=("Segoe UI", 10), bg="#FAFAFA", fg="#333333", selectbackground="#3498DB", relief=tk.FLAT, bd=0, highlightthickness=1, highlightbackground="#E1E1E1")
        self.menu_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        menu_scroll = ttk.Scrollbar(menu_frame, orient="vertical", command=self.menu_listbox.yview)
        menu_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.menu_listbox.config(yscrollcommand=menu_scroll.set)

        for item in self.menu.get_all_items():
            if item.is_available:
                self.menu_listbox.insert(tk.END, f"  {item.name} — ₱{item.price:.2f}  [{item.item_id}]")

        add_btn = tk.Button(left_card, text="+ Add to Order", bg=self.accent_color, fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, cursor="hand2", command=self.add_to_order)
        add_btn.pack(fill=tk.X, padx=15, pady=15)

        # Right Card: Cart and Total
        right_card = tk.Frame(top_section, bg=self.card_bg, highlightbackground="#DCDDE1", highlightthickness=1)
        right_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        tk.Label(right_card, text="Current Order", bg=self.card_bg, fg=self.primary_color, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=15, pady=(15, 10))

        cart_frame = tk.Frame(right_card, bg=self.card_bg)
        cart_frame.pack(fill=tk.BOTH, expand=True, padx=15)

        self.cart_listbox = tk.Listbox(cart_frame, font=("Segoe UI", 10), bg="#FAFAFA", fg="#333333", selectbackground="#3498DB", relief=tk.FLAT, bd=0, highlightthickness=1, highlightbackground="#E1E1E1")
        self.cart_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        cart_scroll = ttk.Scrollbar(cart_frame, orient="vertical", command=self.cart_listbox.yview)
        cart_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.cart_listbox.config(yscrollcommand=cart_scroll.set)

        checkout_panel = tk.Frame(right_card, bg=self.card_bg)
        checkout_panel.pack(fill=tk.X, padx=15, pady=15)

        self.total_label = tk.Label(checkout_panel, text="Total: ₱0.00", bg=self.card_bg, fg="#2C3E50", font=("Segoe UI", 12, "bold"))
        self.total_label.pack(anchor="w", pady=(0, 10))

        pay_btn = tk.Button(checkout_panel, text="Proceed to Checkout", bg=self.button_blue, fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, cursor="hand2", command=self.open_checkout_dialog)
        pay_btn.pack(fill=tk.X)

        # Bottom Section: Terminal/Logs
        log_card = tk.Frame(main_container, bg=self.card_bg, highlightbackground="#DCDDE1", highlightthickness=1)
        log_card.pack(fill=tk.BOTH, expand=True, pady=(15, 0))

        tk.Label(log_card, text="System & Transaction Log", bg=self.card_bg, fg=self.primary_color, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=15, pady=(10, 5))

        log_container = tk.Frame(log_card, bg=self.card_bg)
        log_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        self.log_text = tk.Text(log_container, height=6, font=("Consolas", 9), bg="#1E1E1E", fg="#2ECC71", relief=tk.FLAT, padx=10, pady=10)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        log_scroll = ttk.Scrollbar(log_container, orient="vertical", command=self.log_text.yview)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=log_scroll.set)

    def open_customer_setup_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Customer Information Setup")
        dialog.geometry("400x320")
        dialog.config(bg=self.card_bg)
        dialog.grab_set()

        tk.Label(dialog, text="Enter Customer Details", bg=self.card_bg, fg=self.primary_color, font=("Segoe UI", 12, "bold")).pack(pady=(20, 15))

        form_frame = tk.Frame(dialog, bg=self.card_bg)
        form_frame.pack(fill=tk.X, padx=30)

        tk.Label(form_frame, text="Full Name:", bg=self.card_bg, font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 2))
        name_entry = tk.Entry(form_frame, font=("Segoe UI", 10), width=35)
        name_entry.pack(anchor="w", pady=(0, 10))
        name_entry.insert(0, self.customer.name if self.customer.name != "Guest User" else "Aldwyn Umali")

        tk.Label(form_frame, text="Contact Number:", bg=self.card_bg, font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 2))
        contact_entry = tk.Entry(form_frame, font=("Segoe UI", 10), width=35)
        contact_entry.pack(anchor="w", pady=(0, 10))
        contact_entry.insert(0, self.customer.contact_number)

        tk.Label(form_frame, text="Delivery Address / Location:", bg=self.card_bg, font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 2))
        address_entry = tk.Entry(form_frame, font=("Segoe UI", 10), width=35)
        address_entry.pack(anchor="w", pady=(0, 10))
        address_entry.insert(0, self.customer.address)

        def save_customer_info():
            name = name_entry.get().strip()
            contact = contact_entry.get().strip()
            address = address_entry.get().strip()

            if not name or not contact or not address:
                messagebox.showerror("Validation Error", "All fields are required.", parent=dialog)
                return

            self.customer._name = name
            self.customer._contact_number = contact
            self.customer._address = address

            # Update Header UI display
            self.user_info_label.config(text=f"👤 {self.customer.name} | 📞 {self.customer.contact_number} | 📍 {self.customer.address}")
            self.log_text.insert(tk.END, f"Customer Profile Updated: {self.customer.name} | {self.customer.contact_number} | {self.customer.address}\n")
            self.log_text.see(tk.END)

            dialog.destroy()

        save_btn = tk.Button(dialog, text="Save & Continue", bg=self.accent_color, fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, cursor="hand2", command=save_customer_info)
        save_btn.pack(pady=10)

    def add_to_order(self):
        try:
            selected_idx = self.menu_listbox.curselection()[0]
            selected_text = self.menu_listbox.get(selected_idx)
            item_id = selected_text.split("[")[1].split("]")[0]
            item = self.menu.get_item(item_id)
            
            self.current_order.add_item(item)
            self.cart_listbox.insert(tk.END, f"  {item.name} — ₱{item.price:.2f}")
            self.total_label.config(text=f"Total: ₱{self.current_order.total_amount:.2f}")
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a menu item to add.")

    def open_checkout_dialog(self):
        if not self.current_order._items:
            messagebox.showwarning("Cart Empty", "Your cart is empty. Please add items before checkout.")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Checkout Options")
        dialog.geometry("380x280")
        dialog.config(bg=self.card_bg)
        dialog.grab_set()

        tk.Label(dialog, text="Select Payment Method", bg=self.card_bg, fg=self.primary_color, font=("Segoe UI", 12, "bold")).pack(pady=(20, 10))
        tk.Label(dialog, text=f"Amount Due: ₱{self.current_order.total_amount:.2f}", bg=self.card_bg, fg="#e74c3c", font=("Segoe UI", 11, "bold")).pack(pady=(0, 15))

        payment_var = tk.StringVar(value="COD")

        radio_frame = tk.Frame(dialog, bg=self.card_bg)
        radio_frame.pack(anchor="w", padx=60, pady=5)

        tk.Radiobutton(radio_frame, text="Cash on Delivery (COD)", variable=payment_var, value="COD", bg=self.card_bg, font=("Segoe UI", 10)).pack(anchor="w", pady=2)
        tk.Radiobutton(radio_frame, text="Credit Card", variable=payment_var, value="Card", bg=self.card_bg, font=("Segoe UI", 10)).pack(anchor="w", pady=2)

        def confirm_payment():
            amount = self.current_order.total_amount
            method = payment_var.get()

            if method == "Card":
                card_num = simpledialog.askstring("Credit Card Payment", "Enter 16-digit Card Number:", initialvalue="1234567890123456", parent=self.root)
                dialog.destroy()
                if not card_num:
                    return
                payment = CreditCardPayment(card_num)
                success, log_msg = payment.process_payment(amount)
            else:
                cash_str = simpledialog.askstring("Cash on Delivery", f"Total due is ₱{amount:.2f}.\nEnter Total Amount Pay:", parent=self.root)
                dialog.destroy()
                if cash_str is None:
                    return
                try:
                    cash_tendered = float(cash_str)
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter a valid numeric value.", parent=self.root)
                    return

                payment = CashOnDelivery(cash_tendered)
                success, log_msg = payment.process_payment(amount)
                if not success:
                    messagebox.showerror("Payment Failed", log_msg, parent=self.root)
                    return

            # Generate dynamic timestamps synchronized with the desktop system clock
            t_payment = datetime.now()
            t_preparing = t_payment + timedelta(seconds=15)
            t_pickup = t_preparing + timedelta(seconds=30)
            t_on_way = t_pickup + timedelta(seconds=45)
            t_delivered = t_on_way + timedelta(seconds=60)

            fmt = "%Y-%m-%d %H:%M:%S"

            # Format status lines with respective timestamps
            step1 = f"[{t_payment.strftime(fmt)}] Payment Received & Confirmed. {log_msg}"
            step2 = f"[{t_preparing.strftime(fmt)}] Order Status: Preparing."
            step3 = f"[{t_pickup.strftime(fmt)}] Order Status: Waiting for the rider to pick-up the order."
            step4 = f"[{t_on_way.strftime(fmt)}] Order Status: Rider is on its way to {self.customer.address}."
            step5 = f"[{t_delivered.strftime(fmt)}] Order Status: Delivered Successfully."

            # Push records to the background terminal log
            self.log_text.insert(tk.END, f"{step1}\n")
            self.log_text.insert(tk.END, f"{step2}\n")
            self.log_text.insert(tk.END, f"{step3}\n")
            self.log_text.insert(tk.END, f"{step4}\n")
            self.log_text.insert(tk.END, f"{step5}\n")
            self.log_text.insert(tk.END, "--------------------------------------------------\n")
            self.log_text.see(tk.END)

            # Display transaction receipt/details prominently right in front
            receipt_details = (
                f"=== ORDER RECEIPT & TRANSACTION SUMMARY ===\n\n"
                f"Customer: {self.customer.name}\n"
                f"Contact Number: {self.customer.contact_number}\n"
                f"Delivery Address: {self.customer.address}\n\n"
                f"{step1}\n"
                f"{step2}\n"
                f"{step3}\n"
                f"{step4}\n"
                f"{step5}\n\n"
                f"Status: Completed Successfully!"
            )
            messagebox.showinfo("Transaction Details", receipt_details, parent=self.root)
            
            # Reset order and cart
            self.current_order = Order("ORD1002", self.customer)
            self.cart_listbox.delete(0, tk.END)
            self.total_label.config(text="Total: ₱0.00")

        confirm_btn = tk.Button(dialog, text="Confirm Payment", bg=self.accent_color, fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, cursor="hand2", command=confirm_payment)
        confirm_btn.pack(fill=tk.X, padx=40, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = FoodDeliveryApp(root)
    root.mainloop()