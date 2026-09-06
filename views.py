import tkinter as tk

BG_MAIN = "#EBF5FB"
BG_ADMIN = "#154360"
BTN_PRIMARY = "#2980B9"
BTN_SUCCESS = "#27AE60"
BTN_DANGER = "#E74C3C"
BTN_ACTION = "#F39C12"
TEXT_DARK = "#2C3E50"
TEXT_LIGHT = "#ECF0F1"

class AppView:
    def __init__(self, root):
        self.root = root
        self.root.title("QuickBite MVC App")
        self.root.geometry("850x650") 

        left = tk.Frame(root, padx=15, pady=15, bg=BG_MAIN)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(left, text="Menu (Click Button to Add)", bg=BG_MAIN, fg=TEXT_DARK, font=("Segoe UI", 11, "bold")).pack()
        
        self.menu_frame = tk.Frame(left, bg=BG_MAIN)
        self.menu_frame.pack(fill=tk.X, pady=5)

        tk.Label(left, text="Your Cart:", bg=BG_MAIN, fg=TEXT_DARK, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 0))
        
        # Replaced Listbox with a Frame for dynamic item rows
        self.cart_frame = tk.Frame(left, bg="white", bd=1, relief=tk.SOLID)
        self.cart_frame.pack(fill=tk.X, pady=2, ipady=5)

        tk.Label(left, text="Customer Name:", bg=BG_MAIN, fg=TEXT_DARK, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 0))
        self.entry_name = tk.Entry(left, font=("Segoe UI", 10))
        self.entry_name.pack(fill=tk.X, pady=2)

        tk.Label(left, text="Cart Total:", bg=BG_MAIN, fg=TEXT_DARK).pack(pady=(10, 0))
        self.lbl_total = tk.Label(left, text="₱0.00", fg=TEXT_DARK, bg=BG_MAIN, font=("Segoe UI", 16, "bold"))
        self.lbl_total.pack(pady=5)

        # Single Checkout Button
        self.btn_checkout = tk.Button(left, text="Checkout", bg=BTN_SUCCESS, fg="white", font=("Segoe UI", 10, "bold"))
        self.btn_checkout.pack(fill=tk.X, pady=10)

        right = tk.Frame(root, padx=15, pady=15, bg=BG_ADMIN)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(right, text="Admin: Order & Payment Management", bg=BG_ADMIN, fg=TEXT_LIGHT, font=("Segoe UI", 11, "bold")).pack()
        self.order_list = tk.Listbox(right, height=15, font=("Consolas", 10), bg="white", fg=TEXT_DARK)
        self.order_list.pack(fill=tk.BOTH, expand=True, pady=10)

        self.btn_verify = tk.Button(right, text="Verify Selected Payment", bg=BTN_ACTION, fg="white", font=("Segoe UI", 10, "bold"))
        self.btn_verify.pack(fill=tk.X, pady=5)

        self.btn_update_status = tk.Button(right, text="Manage Order Status", bg=BTN_PRIMARY, fg="white", font=("Segoe UI", 10, "bold"))
        self.btn_update_status.pack(fill=tk.X)

    def open_payment_prompt(self, callback):
        win = tk.Toplevel(self.root)
        win.title("Select Payment")
        win.geometry("250x150")
        win.configure(bg=BG_MAIN)
        win.grab_set() 

        tk.Label(win, text="Choose Payment Method:", bg=BG_MAIN, fg=TEXT_DARK, font=("Segoe UI", 10, "bold")).pack(pady=15)
        
        tk.Button(win, text="Cash", bg=BTN_SUCCESS, fg="white", font=("Segoe UI", 10, "bold"),
                  command=lambda: [callback("Cash"), win.destroy()]).pack(fill=tk.X, padx=30, pady=5)
        tk.Button(win, text="Card", bg=BTN_PRIMARY, fg="white", font=("Segoe UI", 10, "bold"),
                  command=lambda: [callback("Card"), win.destroy()]).pack(fill=tk.X, padx=30, pady=5)

    def open_status_window(self, current_status, update_callback):
        win = tk.Toplevel(self.root)
        win.title("Update Order Status")
        win.geometry("300x280")
        win.configure(bg=BG_MAIN)
        win.grab_set() 

        tk.Label(win, text=f"Current Status:\n{current_status}", bg=BG_MAIN, fg=TEXT_DARK, font=("Segoe UI", 10, "bold")).pack(pady=15)

        statuses = ["Preparing", "Ready for pickup", "On its way", "Delivered"]
        
        for status in statuses:
            btn = tk.Button(
                win, 
                text=status, 
                bg=BTN_PRIMARY, 
                fg="white", 
                font=("Segoe UI", 10, "bold"),
                command=lambda s=status: [update_callback(s), win.destroy()]
            )
            btn.pack(fill=tk.X, padx=30, pady=5)