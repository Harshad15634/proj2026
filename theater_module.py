FILENAME = "tickets.txt"

def save_ticket(play_name, seat, price):

    line = f"{play_name}-{seat}-{price}\n"
    with open(FILENAME, "a") as file:
        file.write(line)

def read_all_tickets():

    try:
        with open(FILENAME, "r") as file:
            return [line.strip().split("-") for line in file.readlines()]
    except FileNotFoundError:
        return []

def search_ticket(term):
 
    all_tickets = read_all_tickets()
    return [t for t in all_tickets if term.lower() in t[0].lower()]

def update_ticket(play_name, new_seat, new_price):

    tickets = read_all_tickets()
    updated = False
    with open(FILENAME, "w") as file:
        for t in tickets:
            if t[0].lower() == play_name.lower():
                file.write(f"{t[0]}-{new_seat}-{new_price}\n")
                updated = True
            else:
                file.write(f"{t[0]}-{t[1]}-{t[2]}\n")
    return updated