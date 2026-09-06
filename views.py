import tkinter as tk

class AppView:
    def __init__(self, root):
        self.root = root
        self.root.title("QuickBite MVC App")
        self.root.geometry("650x450") # Slightly taller to fit the input

        # --- LEFT: CUSTOMER PORTAL ---
        left = tk.Frame(root, padx=15, pady=15, bg="#F4F6F9")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(left, text="Menu (Double-Click to Add)", bg="#F4F6F9", font=("Segoe UI", 10, "bold")).pack()
        self.menu_list = tk.Listbox(left, height=6, font=("Segoe UI", 10))
        self.menu_list.pack(fill=tk.X, pady=5)

        # NEW: Customer Name Input
        tk.Label(left, text="Customer Name:", bg="#F4F6F9", font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(10, 0))
        self.entry_name = tk.Entry(left, font=("Segoe UI", 10))
        self.entry_name.pack(fill=tk.X, pady=2)

        tk.Label(left, text="Cart Total:", bg="#F4F6F9").pack(pady=(10, 0))
        self.lbl_total = tk.Label(left, text="₱0.00", fg="#C0392B", bg="#F4F6F9", font=("Segoe UI", 14, "bold"))
        self.lbl_total.pack(pady=5)

        self.btn_cash = tk.Button(left, text="Pay with Cash", bg="#27AE60", fg="white", font=("Segoe UI", 9, "bold"))
        self.btn_cash.pack(fill=tk.X, pady=2)
        
        self.btn_card = tk.Button(left, text="Pay with Card", bg="#2980B9", fg="white", font=("Segoe UI", 9, "bold"))
        self.btn_card.pack(fill=tk.X, pady=2)

        # --- RIGHT: ADMIN DASHBOARD ---
        right = tk.Frame(root, padx=15, pady=15, bg="#2C3E50")
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(right, text="Admin: Deliveries", bg="#2C3E50", fg="white", font=("Segoe UI", 10, "bold")).pack()
        self.order_list = tk.Listbox(right, height=12, font=("Segoe UI", 9))
        self.order_list.pack(fill=tk.BOTH, expand=True, pady=5)

        self.btn_dispatch = tk.Button(right, text="Update Status -> Delivered", bg="#F39C12", font=("Segoe UI", 9, "bold"))
        self.btn_dispatch.pack(fill=tk.X)