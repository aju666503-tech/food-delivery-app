import tkinter as tk

# Modern Color Palette
BG_APP = "#F1F5F9"            # Slate 100
BG_CARD = "#FFFFFF"           # White
BG_ADMIN = "#0F172A"          # Slate 900
BG_ADMIN_CARD = "#1E293B"     # Slate 800

BTN_PRIMARY = "#3B82F6"       # Blue 500
BTN_PRIMARY_HOVER = "#2563EB" # Blue 600
BTN_SUCCESS = "#10B981"       # Emerald 500
BTN_SUCCESS_HOVER = "#059669" # Emerald 600
BTN_DANGER = "#EF4444"        # Red 500
BTN_DANGER_HOVER = "#DC2626"  # Red 600
BTN_ACTION = "#F59E0B"        # Amber 500
BTN_ACTION_HOVER = "#D97706"  # Amber 600
BTN_MENU = "#E0F2FE"          # Light Blue
BTN_MENU_HOVER = "#BAE6FD"    # Darker Light Blue

TEXT_DARK = "#0F172A"
TEXT_MUTED = "#64748B"
TEXT_LIGHT = "#F8FAFC"

class HoverButton(tk.Button):
    """Custom Tkinter Button with smooth hover animations."""
    def __init__(self, master, bg_color, hover_color, **kwargs):
        tk.Button.__init__(self, master, bg=bg_color, activebackground=hover_color, 
                           relief=tk.FLAT, bd=0, cursor="hand2", **kwargs)
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self.hover_color

    def on_leave(self, e):
        self['background'] = self.bg_color

class AppView:
    def __init__(self, root):
        self.root = root
        self.root.title("QuickBite Modern")
        self.root.geometry("900x650") 
        self.root.configure(bg=BG_APP)

        # --- LEFT: CUSTOMER PORTAL ---
        left = tk.Frame(root, padx=25, pady=25, bg=BG_APP)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(left, text="Our Menu", bg=BG_APP, fg=TEXT_DARK, font=("Segoe UI", 16, "bold")).pack(anchor="w")
        tk.Label(left, text="Click to add items to your cart", bg=BG_APP, fg=TEXT_MUTED, font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 10))
        
        self.menu_frame = tk.Frame(left, bg=BG_APP)
        self.menu_frame.pack(fill=tk.X, pady=5)

        tk.Label(left, text="Your Cart", bg=BG_APP, fg=TEXT_DARK, font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(20, 5))
        
        self.cart_frame = tk.Frame(left, bg=BG_CARD, bd=0, highlightthickness=1, highlightbackground="#E2E8F0")
        self.cart_frame.pack(fill=tk.X, pady=2, ipady=5)

        tk.Label(left, text="Customer Name:", bg=BG_APP, fg=TEXT_DARK, font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(20, 5))
        self.entry_name = tk.Entry(left, font=("Segoe UI", 11), relief=tk.FLAT, highlightthickness=1, highlightbackground="#CBD5E1", bg=BG_CARD)
        self.entry_name.pack(fill=tk.X, ipady=5)

        # Total & Checkout Row
        bottom_frame = tk.Frame(left, bg=BG_APP)
        bottom_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(bottom_frame, text="Total:", bg=BG_APP, fg=TEXT_MUTED, font=("Segoe UI", 12)).pack(side=tk.LEFT)
        self.lbl_total = tk.Label(bottom_frame, text="₱0.00", fg=TEXT_DARK, bg=BG_APP, font=("Segoe UI", 18, "bold"))
        self.lbl_total.pack(side=tk.LEFT, padx=10)

        self.btn_checkout = HoverButton(bottom_frame, bg_color=BTN_SUCCESS, hover_color=BTN_SUCCESS_HOVER, 
                                        text="Checkout Order", fg="white", font=("Segoe UI", 11, "bold"), padx=15, pady=5)
        self.btn_checkout.pack(side=tk.RIGHT)

        # --- RIGHT: ADMIN DASHBOARD ---
        right = tk.Frame(root, padx=25, pady=25, bg=BG_ADMIN)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(right, text="Admin Dashboard", bg=BG_ADMIN, fg=TEXT_LIGHT, font=("Segoe UI", 16, "bold")).pack(anchor="w")
        tk.Label(right, text="Order & Payment Management", bg=BG_ADMIN, fg="#94A3B8", font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 10))
        
        self.order_list = tk.Listbox(right, height=15, font=("Consolas", 10), bg=BG_ADMIN_CARD, fg=TEXT_LIGHT, 
                                     relief=tk.FLAT, bd=0, highlightthickness=1, highlightbackground="#334155", 
                                     selectbackground=BTN_PRIMARY, selectforeground="white", activestyle="none")
        self.order_list.pack(fill=tk.BOTH, expand=True, pady=10)

        admin_btn_frame = tk.Frame(right, bg=BG_ADMIN)
        admin_btn_frame.pack(fill=tk.X, pady=5)

        self.btn_verify = HoverButton(admin_btn_frame, bg_color=BTN_ACTION, hover_color=BTN_ACTION_HOVER, 
                                      text="Verify Selected Payment", fg="white", font=("Segoe UI", 10, "bold"), pady=8)
        self.btn_verify.pack(fill=tk.X, pady=(0, 10))

        self.btn_update_status = HoverButton(admin_btn_frame, bg_color=BTN_PRIMARY, hover_color=BTN_PRIMARY_HOVER, 
                                             text="Manage Order Status", fg="white", font=("Segoe UI", 10, "bold"), pady=8)
        self.btn_update_status.pack(fill=tk.X)

    def open_payment_prompt(self, callback):
        win = tk.Toplevel(self.root)
        win.title("Payment Method")
        win.geometry("300x180")
        win.configure(bg=BG_CARD)
        win.grab_set() 

        tk.Label(win, text="Select Payment Method", bg=BG_CARD, fg=TEXT_DARK, font=("Segoe UI", 12, "bold")).pack(pady=(20, 15))
        
        HoverButton(win, bg_color=BTN_SUCCESS, hover_color=BTN_SUCCESS_HOVER, text="Cash", fg="white", font=("Segoe UI", 10, "bold"),
                    command=lambda: [callback("Cash"), win.destroy()]).pack(fill=tk.X, padx=40, pady=5, ipady=3)
        HoverButton(win, bg_color=BTN_PRIMARY, hover_color=BTN_PRIMARY_HOVER, text="Card", fg="white", font=("Segoe UI", 10, "bold"),
                    command=lambda: [callback("Card"), win.destroy()]).pack(fill=tk.X, padx=40, pady=5, ipady=3)

    def open_status_window(self, current_status, update_callback):
        win = tk.Toplevel(self.root)
        win.title("Update Status")
        win.geometry("300x320")
        win.configure(bg=BG_CARD)
        win.grab_set() 

        tk.Label(win, text="Current Status:", bg=BG_CARD, fg=TEXT_MUTED, font=("Segoe UI", 9)).pack(pady=(20, 0))
        tk.Label(win, text=current_status, bg=BG_CARD, fg=BTN_PRIMARY, font=("Segoe UI", 12, "bold")).pack(pady=(0, 15))

        statuses = ["Preparing", "Ready for pickup", "On its way", "Delivered"]
        
        for status in statuses:
            HoverButton(
                win, bg_color=BTN_APP if status != "Delivered" else BTN_SUCCESS, 
                hover_color=BTN_PRIMARY_HOVER if status != "Delivered" else BTN_SUCCESS_HOVER,
                text=status, fg="white", font=("Segoe UI", 10, "bold"),
                command=lambda s=status: [update_callback(s), win.destroy()]
            ).pack(fill=tk.X, padx=40, pady=5, ipady=4)

# Helper constant for the status window button mapping loop
BTN_APP = BTN_PRIMARY