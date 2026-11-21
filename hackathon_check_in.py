# Hackathon Check-In Tracker
# AM - AI Engineering

# Starter data 
# Tuple: the workshop options are fixed and never change
workshops = ("Game Design", "AI Chatbots", "Robotics")

# Dictionary: student name (key) - assigned workshop (value)
registrations = {
    "maya": "Game Design",
    "jordan": "AI Chatbots",
    "alex": "Robotics",
    "sam": "Game Design",
    "taylor": "AI Chatbots"
}

# Set: names of students who are checked in (no duplicates allowed)
checked_in = set()


# Helper functions 
def print_header(title):
    print()
    print("========== " + title + " ==========")
    print()


def show_menu():
    print_header("HACKATHON CHECK-IN")
    print("1. View Workshops")
    print("2. Look Up a Registration")
    print("3. Check In a Student")
    print("4. View Attendance Report")
    print("5. Remove One Check-In")
    print("6. Clear All Check-Ins")
    print("7. Register a New Student")
    print("8. Change a Student's Workshop")
    print("9. View Check-Ins for One Workshop")
    print("10. Exit")
    print()


def show_workshops(workshop_list):
    number = 1
    for workshop in workshop_list:
        print(str(number) + ". " + workshop)
        number += 1


# Returns the cleaned name. .strip() removes extra spaces and .lower() makes it
# lowercase, so " MAYA " and "maya" are treated as the same student
def get_name():
    while True:
        name = input("Enter student name: ")
        name = name.strip().lower()
        if name == "":
            print("Error: name cannot be empty.")
        else:
            return name


# Returns the workshop name the volunteer picks, asking until the number is valid
def choose_workshop(workshop_list):
    show_workshops(workshop_list)
    while True:
        choice = input("Enter workshop number: ").strip()
        # .isdigit() blocks text like "hello" before int() can crash
        if not choice.isdigit():
            print("Error: please enter a number.")
        elif 1 <= int(choice) <= len(workshop_list):
            # Menu numbers start at 1, but tuple positions start at 0
            return workshop_list[int(choice) - 1]
        else:
            print("Error: choose a number from 1 to " + str(len(workshop_list)) + ".")


# Returns the set of registered students who have not checked in
def find_missing(reg_dict, checked_set):
    all_students = set(reg_dict.keys())
    return all_students - checked_set  # set difference


# Returns the set of checked-in students registered for one workshop
def find_workshop_checkins(reg_dict, checked_set, workshop_name):
    in_workshop = set()
    for name in reg_dict:
        if reg_dict[name] == workshop_name:
            in_workshop.add(name)
    return in_workshop & checked_set  # set intersection


# Returns registered and checked-in counts for every workshop.
# Every workshop starts at 0 so workshops with no students still show up
def count_by_workshop(reg_dict, checked_set, workshop_list):
    counts = {}
    for workshop in workshop_list:
        counts[workshop] = {"registered": 0, "checked_in": 0}
    for name in reg_dict:
        workshop = reg_dict[name]
        counts[workshop]["registered"] += 1
        if name in checked_set:
            counts[workshop]["checked_in"] += 1
    return counts


# Menu option functions 
def look_up_registration():
    name = get_name()
    if name in registrations:
        print("Workshop: " + registrations[name])
    else:
        print("Student not found.")


def check_in_student():
    name = get_name()
    # Conditions must be checked in this order
    if name not in registrations:
        print("Student not found.")
    elif name in checked_in:
        print("This student is already checked in.")
    else:
        checked_in.add(name)
        print(name.title() + " is now checked in.")


def view_attendance_report():
    missing = find_missing(registrations, checked_in)

    print_header("ATTENDANCE REPORT")
    print("Registered students: " + str(len(registrations)))
    print("Checked in: " + str(len(checked_in)))
    print("Still waiting for: " + str(len(missing)))
    if len(missing) == 0:
        print("Everyone is checked in!")
    else:
        print()
        # sorted() gives alphabetical order because sets have no order of their own
        for name in sorted(missing):
            print("- " + name.title())

    # Extra credit: recalculated everytime so it is never out of date
    counts = count_by_workshop(registrations, checked_in, workshops)
    print_header("ATTENDANCE BY WORKSHOP")
    for workshop in workshops:
        print(workshop + " — " + str(counts[workshop]["registered"]) + " registered, "
              + str(counts[workshop]["checked_in"]) + " checked in")


def remove_one_checkin():
    # .pop() crashes on an empty set so check first
    if len(checked_in) == 0:
        print("There are no check-ins to remove.")
    else:
        removed = checked_in.pop()
        print("Removed check-in for " + removed.title() + ".")


def clear_all_checkins():
    while True:
        answer = input("Are you sure you want to clear all check-ins? (yes/no): ")
        answer = answer.strip().lower()
        if answer == "yes":
            checked_in.clear()
            print("All check-ins have been cleared.")
            return
        elif answer == "no":
            print("Reset canceled.")
            return
        else:
            print("Error: please enter yes or no.")


def register_new_student():
    name = get_name()
    if name in registrations:
        print("This student is already registered.")
        return  # go back to the main menu
    workshop = choose_workshop(workshops)
    registrations[name] = workshop
    print(name.title() + " is registered for " + workshop + ".")


def change_workshop():
    name = get_name()
    if name not in registrations:
        print("Student not found.")
        return
    print("Current workshop: " + registrations[name])
    new_workshop = choose_workshop(workshops)
    # Only the value changes, so the student stays checked in
    registrations[name] = new_workshop
    print(name.title() + " is now in " + new_workshop + ".")


def view_workshop_checkins():
    workshop = choose_workshop(workshops)
    students = find_workshop_checkins(registrations, checked_in, workshop)

    print_header(workshop.upper() + " CHECK-INS")
    if len(students) == 0:
        print("Nobody has checked in for this workshop yet.")
    else:
        print("Checked in: " + str(len(students)))
        for name in sorted(students):
            print("- " + name.title())


#  Main program 
def main():
    running = True
    while running:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_workshops(workshops)
        elif choice == "2":
            look_up_registration()
        elif choice == "3":
            check_in_student()
        elif choice == "4":
            view_attendance_report()
        elif choice == "5":
            remove_one_checkin()
        elif choice == "6":
            clear_all_checkins()
        elif choice == "7":
            register_new_student()
        elif choice == "8":
            change_workshop()
        elif choice == "9":
            view_workshop_checkins()
        elif choice == "10":
            print("Goodbye! Thanks for volunteering!")
            running = False
        else:
            print("Error: invalid choice. Please enter a number from 1 to 10.")


main()


# Reflection Questions 

# 1. Why is a tuple a good choice for the workshop names? When would a list be better?
# A tuple cannot be changed, which fits because the workshop names are fixed and
# should not be edited while the program runs. A list would be better if the
# workshops needed to change, like adding or removing one.

# 2. What changes in the dictionary when you register a new student? When you move a student?
# Registering adds a new key (the name) with its workshop as the value. 
# Moving a student keeps the same key and only changes its value to the new workshop.

# 3. Which menu option uses set difference, and which uses set intersection?
# Option 4 (Attendance Report) uses set difference. It finds students who are
# registered but have not checked in.
# Option 9 (View Check-Ins for One Workshop) uses set intersection. It finds students
# who are both registered for that workshop and checked in.

# 4. What does .pop() return? Why check if the set is empty before calling it?
# .pop() removes one arbitrary item from the set and returns it. On an empty set it
# causes a KeyError and the program crashes, so we check for an empty set first.

# 5. After using .clear(), what happens to the check-ins and the registrations?
# The check-ins set becomes empty, so there are zero check-ins. The registrations
# dictionary is unchanged, so every student stays registered and appears under
# "Still waiting for."