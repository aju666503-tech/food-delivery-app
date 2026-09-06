from abc import ABC, abstractmethod

# ---------------------------------------------------------
# 1. Abstraction & Inheritance (Customer Management Module)
# ---------------------------------------------------------
class User(ABC):
    def __init__(self, name):
        self._name = name  # Encapsulation

    @property
    def name(self):
        return self._name

    @abstractmethod
    def get_role(self):
        pass

class Customer(User):
    def __init__(self, name, address):
        super().__init__(name)
        self._address = address

    @property
    def address(self):
        return self._address

    def get_role(self):
        return "Customer"


# ---------------------------------------------------------
# 2. Encapsulation (Menu & Order Processing Modules)
# ---------------------------------------------------------
class FoodOrder:
    MENU = {"Burger": 150.0, "Fries": 80.0, "Wings": 220.0, "Latte": 180.0}

    def __init__(self, customer=None): # Allow empty initialization
        self._customer = customer
        self._items = []
        self.status = "Pending"

    def add_item(self, item_name):
        if item_name in self.MENU:
            self._items.append(item_name)

    @property
    def total(self):
        return sum(self.MENU[i] for i in self._items)

    @property
    def customer(self):
        return self._customer

    @customer.setter
    def customer(self, new_customer): # Allows setting customer at checkout
        self._customer = new_customer

# ---------------------------------------------------------
# 3. Polymorphism (Payment & Delivery Module)
# ---------------------------------------------------------
class Payment(ABC):
    @abstractmethod
    def process(self, amount):
        pass

class CashPayment(Payment):
    def process(self, amount):
        return f"Paid ₱{amount:.2f} via Cash on Delivery."

class CardPayment(Payment):
    def process(self, amount):
        return f"Paid ₱{amount:.2f} via Credit Card." 
    
    