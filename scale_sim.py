import models
import time


def simulate_value(slot, value):
    print(f"Weight simulated as {value}")
    slot.update(value)
    time.sleep(1)


def main():
    item = models.Item(1, 'test', '', 3, 20, 226, 10, '', '')
    items = [item]
    shelf = models.Shelf(items)
    slot = models.Slot(shelf, item)
    # slot.set_conversion_factor(0.22668)

    simulate_value(slot, 4)
    simulate_value(slot, 4)
    simulate_value(slot, 4)
    simulate_value(slot, 230)
    simulate_value(slot, 230)
    simulate_value(slot, 230)
    simulate_value(slot, 2)
    simulate_value(slot, 2)
    simulate_value(slot, 2)
    simulate_value(slot, 2)
    simulate_value(slot, 2)
    simulate_value(slot, 2)
    simulate_value(slot, 2)
    simulate_value(slot, 4)
    simulate_value(slot, 4)
    simulate_value(slot, 4)
    simulate_value(slot, 2)
    simulate_value(slot, 2)
    simulate_value(slot, 2)
    simulate_value(slot, 2)









if __name__ == '__main__':
    main()

