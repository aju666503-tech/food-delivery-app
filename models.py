from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, name):
        self._name = name  

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


class FoodOrder:
    MENU = {"Burger": 150.0, "Fries": 80.0, "Wings": 220.0, "Latte": 180.0}

    def __init__(self, customer=None): 
        self._customer = customer
        self._items = {}  # Changed to a dictionary to track quantities
        self.status = "Pending"
        self.payment_method = None
        self.time_left = 0
        self.receipt = None 

    def add_item(self, item_name):
        if item_name in self.MENU:
            self._items[item_name] = self._items.get(item_name, 0) + 1

    def remove_item(self, item_name):
        if item_name in self._items:
            self._items[item_name] -= 1
            if self._items[item_name] <= 0:
                del self._items[item_name]

    @property
    def total(self):
        return sum(self.MENU[item] * qty for item, qty in self._items.items())

    @property
    def customer(self):
        return self._customer

    @customer.setter
    def customer(self, new_customer): 
        self._customer = new_customer


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