class User:
    def __init__(self, uid, name, balance, payment_type):
        self.uid = uid
        self.name = name
        self.balance = balance
        self.payment_type = payment_type
        self.email = ""
        self.phone = ""


class Item:
    def __init__(self, name, price, avg_weight, std_weight):
        self.name = name
        self.price = price
        self.avg_weight = avg_weight
        self.std_weight = std_weight


class Stock:
    def __init__(self):
        self.items = {}         # Item: quantity

    def add(self, item: Item, quantity: int):
        if item in self.items:
            self.items[item] += 1
        else:
            self.items[item] = 1


class Cart:
    def __init__(self):
        self.items = {}         # Item: quantity
        self.payment = False

    def add(self, item: Item):
        if item in self.items:
            self.items[item] += 1
        else:
            self.items[item] = 1

    def remove(self, item: Item):
        if item in self.items:
            self.items[item] -= 1

    def get_subtotal(self):
        subtotal = 0.0

        for item, quantity in self.items.items():
            subtotal += item.price * quantity

        return subtotal
