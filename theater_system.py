"""Movie theater seat reservation system."""
import hashlib
import json
import os

SEATS_FILE = "seats.json"

# Global state
SHOWS = {
    "SHOW-1": {"title": "Interstellar", "seats": 20, "booked": []},
    "SHOW-2": {"title": "Dangal", "seats": 10, "booked": []},
}

def reserve_seat(show_id, seat_number, system_logs=None):
    """Reserve a seat. Return True on success, False otherwise."""
    if system_logs is None:
        system_logs = []

    show = SHOWS.get(show_id)
    if show is None:
        system_logs.append(f"Unknown show {show_id}")
        return False

    if isinstance(seat_number, bool) or not isinstance(seat_number, int):
        system_logs.append(f"Invalid seat {seat_number!r} for {show_id}")
        return False

    if not 1 <= seat_number <= show["seats"]:
        system_logs.append(f"Seat {seat_number} out of range for {show_id}")
        return False

    if seat_number in show["booked"]:
        system_logs.append(f"Seat {seat_number} already taken for {show_id}")
        return False

    show["booked"].append(seat_number)
    system_logs.append(f"Reserved seat {seat_number} for {show_id}")
    return True

def release_seat(show_id, seat_number):
    """Release a booked seat. Return True if it was booked."""
    try:
        SHOWS[show_id]["booked"].remove(seat_number)
    except (KeyError, ValueError):
        return False
    return True

def ticket_code(show_id, seat_number):
    """Return a short ticket code for a show and seat."""
    raw = f"{show_id}{seat_number}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:8]

def dump_reservations(filename=SEATS_FILE):
    """Save the seating plan to a JSON file."""
    with open(filename, "w", encoding="utf-8") as file_obj:
        json.dump(SHOWS, file_obj)

def load_reservations(filename=SEATS_FILE):
    """Load the seating plan from a JSON file."""
    with open(filename, "r", encoding="utf-8") as file_obj:
        data = json.load(file_obj)
    SHOWS.clear()
    SHOWS.update(data)

def print_seating_summary():
    """Print free seats and booked seats for every show."""
    for show in SHOWS.values():
        free = show["seats"] - len(show["booked"])
        print(f"{show['title']}: {free} seats free, booked = {sorted(show['booked'])}")

def read_seat_choice(prompt, default=4):
    """Read a seat number from the user; fall back to the default."""
    text = input(prompt).strip()
    if not text:
        return default
    try:
        return int(text)
    except ValueError:
        return None

def main():
    """Run the demo."""
    logs = []
    reserve_seat("SHOW-1", 5, logs)
    reserve_seat("SHOW-1", 5, logs)
    reserve_seat("SHOW-1", 25, logs)
    reserve_seat("SHOW-2", -1, logs)
    reserve_seat("SHOW-2", "A7", logs)
    release_seat("SHOW-2", 3)
    print("Ticket code:", ticket_code("SHOW-1", 5))

    seat = read_seat_choice("Seat number to book for SHOW-2 (Enter for 4): ")
    reserve_seat("SHOW-2", seat, logs)

    dump_reservations()
    load_reservations()
    print_seating_summary()

    os.chmod(SEATS_FILE, 0o600)
    print("\nLog:")
    for entry in logs:
        print(" -", entry)

if __name__ == "__main__":
    main()
