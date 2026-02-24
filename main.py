import theater_module
import matplotlib.pyplot as plt

def show_chart():
    data = theater_module.read_tickets()
    if not data:
        print("\nNo tickets found!")
        return

    counts = {}
    for t in data:
        play_name = t[0]
        counts[play_name] = counts.get(play_name, 0) + 1

    names = list(counts.keys())
    totals = list(counts.values())

    plt.figure(figsize=(7, 7))
    plt.pie(totals, labels=names, autopct='%1.1f%%', startangle=140)
    plt.title("Ticket Sales Overview")
    plt.show()

def menu():
    while True:
        print("\n--- THEATRE MANAGEMENT SYSTEM ---")
        print("1. Sell New Ticket")
        print("2. Search for a Play")
        print("3. Update a Ticket")
        print("4. View All Tickets & Chart")
        print("5. Exit")
        
        user_choice = input("\nPick an option: ")

        if user_choice == "1":
            p = input("Play Name: ")
            s = input("Seat Number: ")
            pr = input("Price: ")
            theater_module.save_ticket(p, s, pr)
            print("Done!")

        elif user_choice == "2":
            query = input("Search play: ")
            found = theater_module.find_tickets(query)
            if found:
                for item in found:
                    print(f"{item[0]} | Seat: {item[1]} | Price: {item[2]}")
            else:
                print("No matches.")

        elif user_choice == "3":
            all_tix = theater_module.read_tickets()
            if not all_tix:
                print("List is empty.")
                continue
            
            for i in range(len(all_tix)):
                t = all_tix[i]
                print(f"{i+1}) {t[0]} - Seat: {t[1]} - Price: {t[2]}")
            
            try:
                pick = int(input("\nSelect ID: ")) - 1
                new_n = input("New Name: ")
                new_s = input("New Seat: ")
                new_p = input("New Price: ")
                
                if theater_module.update_specific_ticket(pick, new_n, new_s, new_p):
                    print("Updated!")
                else:
                    print("Invalid ID.")
            except ValueError:
                print("Error: Enter a number.")

        elif user_choice == "4":
            all_tix = theater_module.read_tickets()
            for t in all_tix:
                print(f"{t[0]} | {t[1]} | {t[2]}€")
            show_chart()

        elif user_choice == "5":
            break
        else:
            print("Try again.")

menu()