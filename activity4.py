import csv

INVENTORY = {}

class Article:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price

    def getQuantity(self):
        return self.quantity

    def setQuantity(self, quantity):
        self.quantity = quantity

    def __str__(self):
        return f"Article: {self.name} Quantity: {self.quantity} Price: {self.price}"

def menu():
    print("1. List all items, inventory, and prices")
    print("2. List cart shopping items")
    print("3. Add an item to the shopping cart")
    print("4. Remove an item from the shopping cart")
    print("5. Checkout")
    print("6. Exit")

def read_data():
    try:
        with open('products.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                name = row[0]
                price = float(row[1])
                quantity = int(row[2])
                INVENTORY[name] = Article(name, price, quantity)
    except FileNotFoundError:
        print("Error: File 'products.csv' not found.")
    except StopIteration:
        print("Error: File 'products.csv' is empty.")

def Listed_items():
    with open('products.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            name = row[0]
            price = float(row[1])
            quantity = int(row[2])
            print(f"Article: {name} Quantity: {quantity} Price: {price}")

def Shopping_cart(cart):
    if cart:
        for item in cart:
            print(item)
    else:
        print("Currently the shopping cart has no items in it.")

def Adding_item_to_shopping_cart(cart):
    while True:
        item_name = input("Add an item from our catalogue to the shopping cart: ")
        if item_name in INVENTORY:
            quantity = input("Add the quantity of " + item_name + " : ")
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    print("Quantity should be a positive integer.")
                    continue
            except ValueError:
                print("Invalid quantity. Please enter a number.")
                continue
            if quantity <= INVENTORY[item_name].getQuantity():
                cart.append((item_name, quantity))
                INVENTORY[item_name].setQuantity(INVENTORY[item_name].getQuantity() - quantity)
                break
            else:
                print("Insufficient quantity of ", item_name, " in stock.")
        else:
            print("Item not found in inventory.")

def Item_removal_from_shopping_cart(cart):
    if cart:
        item_name = input("Which item do you want to remove from the shopping cart: ")
        for i, item in enumerate(cart):
            if item[0] == item_name:
                quantity = int(input("Remove the quantity of " + item_name + " from the shopping cart: "))
                if quantity <= item[1]:
                    cart[i] = (item[0], item[1] - quantity)
                    if cart[i][1] == 0:
                        del cart[i]
                    INVENTORY[item_name].setQuantity(INVENTORY[item_name].getQuantity() + quantity)
                    break
                else:
                    print("Invalid quantity to remove for", item_name)
                    break
        else:
            print("Item not found in the shopping cart.")
    else:
        print("Sorry, the shopping cart is empty.")

def Total_sum(cart):
    total = 0
    for product in cart:
        total += product[1] * INVENTORY[product[0]].getPrice()
    for product in cart:
        if product[1] >= 3:
            discount = product[1] * INVENTORY[product[0]].getPrice() * 0.10
            total -= discount
    tax = total * 0.07
    total += tax
    return total

def main():
    read_data()
    menu()

    cart = []
    while True:
        choice = input("Enter your choice: ")

        if choice == '1':
            Listed_items()
        elif choice == '2':
            Shopping_cart(cart)
        elif choice == '3':
            Adding_item_to_shopping_cart(cart)
        elif choice == '4':
            Item_removal_from_shopping_cart(cart)
        elif choice == '5':
            total_price = Total_sum(cart)
            print("Your total bill is: $", total_price)
            confirm = input("Are you sure you want to checkout and clear the cart? (yes/no) ")
            if confirm.lower() == 'yes':
                cart.clear()
                print("Thank you for shopping with us! Your cart is now empty.")
        elif choice == '6':
            break
        else:
            print("Please choose from the given options")

if __name__ == "__main__":
    main()