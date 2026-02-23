import theater_module 
import matplotlib.pyplot as plt

def draw_sales_chart():
 
    tickets = theater_module.read_all_tickets()
    
    if not tickets:
        print("No data available to create a chart.")
        return
    
  
    sales_data = {}
    for t in tickets:
        play_name = t[0]
        sales_data[play_name] = sales_data.get(play_name, 0) + 1

    # Prepare data for Matplotlib
    labels = list(sales_data.keys())
    sizes = list(sales_data.values())

    # Create the Pie Chart
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Ticket Sales Distribution by Play")
    
    print("Opening chart window...")
    plt.show()

def main():
    while True:
        print("\n--- THEATRE TICKET SYSTEM ---")
        print("1 - Create Ticket")
        print("2 - Search Ticket")
        print("3 - Update Ticket")
        print("4 - Consult All & Show Sales Chart") # Pie chart added here
        print("5 - Exit")
        
        choice = input("\nSelect an option: ")

        if choice == "1":
            play = input("Enter Play Name: ")
            seat = input("Enter Seat (e.g. A1): ")
            price = input("Enter Price: ")
            theater_module.save_ticket(play, seat, price)
            print("Ticket saved.")

        elif choice == "2":
            term = input("Search Play Name: ")
            results = theater_module.search_ticket(term)
            for r in results:
                print(f"Found: {r[0]} | Seat: {r[1]} | Price: {r[2]}€")

        elif choice == "3":
            play = input("Play name to update: ")
            new_seat = input("New seat: ")
            new_price = input("New price: ")
            if theater_module.update_ticket(play, new_seat, new_price):
                print("Update successful.")
            else:
                print("Play not found.")

        elif choice == "4":
            print("\nListing all records:")
            all_tix = theater_module.read_all_tickets()
            for t in all_tix:
                print(f"Play: {t[0]} | Seat: {t[1]} | Price: {t[2]}€")
            
        
            draw_sales_chart()

        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()