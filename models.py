class User:
    def __init__(self, uid, name, token, balance, payment_type, email, phone):
        self.uid = uid
        self.name = name
        self.token = token
        self.balance = balance
        self.payment_type = payment_type
        self.email = email
        self.phone = phone


class Item:
    def __init__(
            self, item_id, name, upc, price, units, avg_weight, std_weight,
            thumbnail, vision_class
    ):
        self.item_id = item_id
        self.name = name
        self.upc = upc
        self.price = price
        self.units = units
        self.avg_weight = avg_weight
        self.std_weight = std_weight
        self.thumbnail = thumbnail
        self.vision_class = vision_class


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
