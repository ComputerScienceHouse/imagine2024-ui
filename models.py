
WEIGHT_UNIT = "g"


class User:
    def __init__(self, uid, name, token, balance, payment_type, email, phone):
        self.uid = uid
        self.name = name
        self.token = token
        self.balance = balance
        self.payment_type = payment_type
        self.email = email
        self.phone = phone

    def __eq__(self, other):
        if isinstance(other, User):
            return (self.uid == other.uid
                    and self.name == other.name
                    and self.token == other.token
                    and self.balance == other.balance
                    and self.payment_type == other.payment_type
                    and self.email == other.email
                    and self.phone == other.phone)
        else:
            return False

    def __str__(self):
        return (f'User[{self.uid},{self.name},{self.token},${self.balance},'
                f'{self.payment_type},{self.email},{self.phone}]')


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

    def __eq__(self, other):
        if isinstance(other, Item):
            return (self.item_id == other.item_id
                    and self.name == other.name
                    and self.upc == other.upc
                    and self.price == other.price
                    and self.units == other.units
                    and self.avg_weight == other.avg_weight
                    and self.std_weight == other.std_weight
                    and self.thumbnail == other.thumbnail
                    and self.vision_class == other.vision_class)
        else:
            return False

    def __str__(self):
        return (f'Item[{self.item_id},{self.name},UPC:{self.upc},${self.price},'
                f'{self.units}units,{self.avg_weight}{WEIGHT_UNIT},'
                f'{self.std_weight}{WEIGHT_UNIT},{self.thumbnail},'
                f'{self.vision_class}]')


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
