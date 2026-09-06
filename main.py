from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, user_id, name, email):
        self._user_id = user_id
        self._name = name
        self._email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @abstractmethod
    def display_role(self):
        pass

class Customer(User):
    def __init__(self, user_id, name, email, address, contact_number):
        super().__init__(user_id, name, email)
        self._address = address
        self._contact_number = contact_number
        self._order_history = []

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, new_address):
        self._address = new_address

    @property
    def contact_number(self):
        return self._contact_number

    @contact_number.setter
    def contact_number(self, new_contact):
        self._contact_number = new_contact

    def add_order(self, order):
        self._order_history.append(order)

    def display_role(self):
        return "Customer"

class MenuItem:
    def __init__(self, item_id, name, price, category):
        self._item_id = item_id
        self._name = name
        self._price = price
        self._category = category
        self._is_available = True

    @property
    def item_id(self):
        return self._item_id

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def is_available(self):
        return self._is_available

    @is_available.setter
    def is_available(self, status):
        self._is_available = status

class Menu:
    def __init__(self):
        self._items = {}

    def add_item(self, item):
        self._items[item.item_id] = item

    def get_item(self, item_id):
        return self._items.get(item_id)

    def get_all_items(self):
        return self._items.values()

class Order:
    def __init__(self, order_id, customer):
        self._order_id = order_id
        self._customer = customer
        self._items = []
        self._status = "Pending"

    def add_item(self, item, quantity=1):
        for _ in range(quantity):
            self._items.append(item)

    @property
    def total_amount(self):
        return sum(item.price for item in self._items)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        self._status = new_status

    def get_order_details(self):
        item_summary = ", ".join([item.name for item in self._items])
        return f"Order ID: {self._order_id} | Customer: {self._customer.name} | Contact: {self._customer.contact_number} | Items: [{item_summary}] | Total: ₱{self.total_amount:.2f} | Status: {self._status}"

class Payment(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCardPayment(Payment):
    def __init__(self, card_number):
        self._card_number = card_number

    def process_payment(self, amount):
        return True, f"Processing credit card payment of ₱{amount:.2f} using card ending in {self._card_number[-4:]}."

class CashOnDelivery(Payment):
    def __init__(self, cash_tendered):
        self._cash_tendered = cash_tendered

    def process_payment(self, amount):
        if self._cash_tendered < amount:
            return False, "Insufficient cash tendered."
        change = self._cash_tendered - amount
        return True, f"Cash on Delivery selected. Tendered: ₱{self._cash_tendered:.2f} | Change: ₱{change:.2f}"

class Delivery:
    def __init__(self, order, delivery_address):
        self._order = order
        self._address = delivery_address
        self._status = "Preparing"

    def update_delivery_status(self, status):
        self._status = status
        return f"Delivery status update: {self._status}"

    def dispatch(self):
        self._status = "Out for Delivery"
        return f"Rider dispatched to: {self._address}. Status: {self._status}"