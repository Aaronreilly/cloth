class ClothingItem:
    def __init__(self, item_id, name, category, size, color, price, stock):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.size = size
        self.color = color
        self.price = price
        self.stock = stock

    def __str__(self):
        return f"ID: {self.item_id}, Name: {self.name}, Category: {self.category}, Size: {self.size}, Color: {self.color}, Price: ₹{self.price:.2f}, Stock: {self.stock}"

    def update_stock(self, quantity):
        self.stock += quantity
        if self.stock < 0:
            self.stock = 0
            print(f"Warning: Stock for {self.name} cannot be negative. Stock set to 0.")

class Customer:
    def __init__(self, customer_id, name, contact):
        self.customer_id = customer_id
        self.name = name
        self.contact = contact

    def __str__(self):
        return f"ID: {self.customer_id}, Name: {self.name}, Contact: {self.contact}"
# Function for purchase
class Purchase:
    def __init__(self, purchase_id, customer, items):
        self.purchase_id = purchase_id
        self.customer = customer
        self.items = items  # Dictionary of {item_id: quantity}
        self.purchase_date = self.get_current_date()

    def get_current_date(self):
        import datetime
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    def calculate_total(self, inventory):
        total = 0
        for item_id, quantity in self.items.items():
            if item_id in inventory:
                total += inventory[item_id].price * quantity
            else:
                print(f"Warning: Item with ID {item_id} not found in inventory.")
        return total

    def __str__(self):
        item_details = ", ".join([f"ID: {item_id}, Qty: {qty}" for item_id, qty in self.items.items()])
        return f"Purchase ID: {self.purchase_id}, Customer: {self.customer.name}, Items: [{item_details}], Date: {self.purchase_date}, Total: ₹{self.calculate_total(inventory):.2f}"

class InventorySystem:
    def __init__(self):
        self.inventory = {}  # Dictionary to store ClothingItem objects, keyed by item_id
        self.customers = {}  # Dictionary to store Customer objects, keyed by customer_id
        self.purchases = []  # List to store Purchase objects
        self.next_item_id = 1
        self.next_customer_id = 1
        self.next_purchase_id = 1

    def add_item(self, name, category, size, color, price, stock):
        new_item = ClothingItem(self.next_item_id, name, category, size, color, price, stock)
        self.inventory[self.next_item_id] = new_item
        self.next_item_id += 1
        print(f"Item '{name}' added to inventory with ID {new_item.item_id}.")

    def view_inventory(self):
        if not self.inventory:
            print("Inventory is empty.")
            return
        print("\n--- Current Inventory ---")
        for item in self.inventory.values():
            print(item)
        print("-----------------------")

    def update_item_stock(self, item_id, quantity_change):
        if item_id in self.inventory:
            self.inventory[item_id].update_stock(quantity_change)
            print(f"Stock for item ID {item_id} updated.")
        else:
            print(f"Error: Item with ID {item_id} not found in inventory.")

    def search_item(self, query, search_by="name"):
        results = []
        query = query.lower()
        for item in self.inventory.values():
            if search_by == "name" and query in item.name.lower():
                results.append(item)
            elif search_by == "category" and query in item.category.lower():
                results.append(item)
            elif search_by == "color" and query in item.color.lower():
                results.append(item)
            elif search_by == "id" and str(item.item_id) == query:
                results.append(item)

        if results:
            print("\n--- Search Results ---")
            for item in results:
                print(item)
            print("----------------------")
        else:
            print(f"No items found matching your search for '{query}' in '{search_by}'.")

    def add_customer(self, name, contact):
        new_customer = Customer(self.next_customer_id, name, contact)
        self.customers[self.next_customer_id] = new_customer
        self.next_customer_id += 1
        print(f"Customer '{name}' added with ID {new_customer.customer_id}.")

    def view_customers(self):
        if not self.customers:
            print("No customers registered.")
            return
        print("\n--- Registered Customers ---")
        for customer in self.customers.values():
            print(customer)
        print("--------------------------")

    def record_purchase(self, customer_id, items_to_purchase):
        if customer_id not in self.customers:
            print(f"Error: Customer with ID {customer_id} not found.")
            return

        purchase_items = {}
        for item_id_str, quantity in items_to_purchase.items():
            try:
                item_id = int(item_id_str)
                quantity = int(quantity)
                if item_id in self.inventory:
                    if self.inventory[item_id].stock >= quantity:
                        purchase_items[item_id] = quantity
                        self.inventory[item_id].update_stock(-quantity)
                    else:
                        print(f"Error: Not enough stock for item ID {item_id} ({self.inventory[item_id].name}). Available: {self.inventory[item_id].stock}, Requested: {quantity}")
                        return
                else:
                    print(f"Error: Item with ID {item_id} not found in inventory.")
                    return
            except ValueError:
                print("Error: Invalid item ID or quantity.")
                return

        if purchase_items:
            new_purchase = Purchase(self.next_purchase_id, self.customers[customer_id], purchase_items)
            self.purchases.append(new_purchase)
            self.next_purchase_id += 1
            print("\n--- Purchase Recorded ---")
            print(new_purchase)
            print("-------------------------")

    def view_purchases(self):
        if not self.purchases:
            print("No purchase history available.")
            return
        print("\n--- Purchase History ---")
        for purchase in self.purchases:
            print(purchase)
        print("----------------------")

def main():
    store = InventorySystem()

    # Adding some initial inventory
    store.add_item("T-Shirt", "Top", "M", "Blue", 599.99, 50)
    store.add_item("Jeans", "Bottom", "32", "Denim", 1299.00, 30)
    store.add_item("Dress", "Outfit", "S", "Red", 1999.50, 20)
    store.add_item("Shirt", "Top", "L", "White", 799.00, 40)

    # Adding some customers
    store.add_customer("Alice Smith", "9876543210")
    store.add_customer("Bob Johnson", "8765432109")

    while True:
        print("\n--- Clothing Store Inventory System ---")
        print("1. Add Item to Inventory")
        print("2. View Inventory")
        print("3. Update Item Stock")
        print("4. Search Item")
        print("5. Add Customer")
        print("6. View Customers")
        print("7. Record Purchase")
        print("8. View Purchase History")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter item name: ")
            category = input("Enter item category: ")
            size = input("Enter item size: ")
            color = input("Enter item color: ")
            try:
                price = float(input("Enter item price: "))
                stock = int(input("Enter initial stock quantity: "))
                store.add_item(name, category, size, color, price, stock)
            except ValueError:
                print("Invalid input for price or stock.")

        elif choice == '2':
            store.view_inventory()

        elif choice == '3':
            try:
                item_id = int(input("Enter item ID to update stock: "))
                quantity_change = int(input("Enter quantity change (positive for addition, negative for removal): "))
                store.update_item_stock(item_id, quantity_change)
            except ValueError:
                print("Invalid input for item ID or quantity.")

        elif choice == '4':
            search_query = input("Enter search term: ")
            search_by = input("Search by (name/category/color/id): ").lower()
            store.search_item(search_query, search_by)

        elif choice == '5':
            name = input("Enter customer name: ")
            contact = input("Enter customer contact number: ")
            store.add_customer(name, contact)

        elif choice == '6':
            store.view_customers()

        elif choice == '7':
            store.view_customers()
            try:
                customer_id = int(input("Enter customer ID for the purchase: "))
                items_to_purchase = {}
                while True:
                    item_id_str = input("Enter item ID to purchase (or 'done' to finish): ")
                    if item_id_str.lower() == 'done':
                        break
                    quantity_str = input(f"Enter quantity for item ID {item_id_str}: ")
                    items_to_purchase[item_id_str] = quantity_str
                if items_to_purchase:
                    store.record_purchase(customer_id, items_to_purchase)
                else:
                    print("No items added to the purchase.")
            except ValueError:
                print("Invalid customer ID.")

        elif choice == '8':
            store.view_purchases()

        elif choice == '9':
            print("Exiting the Clothing Store Inventory System. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
