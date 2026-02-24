FILE_NAME = "tickets.txt"

def save_ticket(play, seat, price):
    with open(FILE_NAME, "a") as f:
        f.write(f"{play}-{seat}-{price}\n")

def read_tickets():
    ticket_list = []
    try:
        with open(FILE_NAME, "r") as f:
            for line in f:
                data = line.strip().split("-")
                if len(data) == 3:
                    ticket_list.append(data)
    except FileNotFoundError:
        return []
    return ticket_list

def find_tickets(search_term):
    all_data = read_tickets()
    results = []
    for t in all_data:
        if search_term.lower() in t[0].lower():
            results.append(t)
    return results

def update_specific_ticket(index, new_name, new_seat, new_price):
    all_data = read_tickets()
    
    if 0 <= index < len(all_data):
        all_data[index][0] = new_name
        all_data[index][1] = new_seat
        all_data[index][2] = new_price
        
        with open(FILE_NAME, "w") as f:
            for t in all_data:
                f.write(f"{t[0]}-{t[1]}-{t[2]}\n")
        return True
    return False