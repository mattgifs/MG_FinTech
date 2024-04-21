import json

def load_data():
    try:
        with open('strength_training_data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data

def save_data(data):
    with open('strength_training_data.json', 'w') as file:
        json.dump(data, file)

def add_training_data(data):
    exercise = input("Enter the exercise name: ")
    day = input("Enter the day of the week (e.g., Monday, Tuesday, etc.): ")
    date = input("Enter the date (e.g., MM/DD/YYYY): ")
    sets = int(input("Enter the number of sets: "))

    if day not in data:
        data[day] = {}

    if exercise not in data[day]:
        data[day][exercise] = []

    for set_num in range(1, sets + 1):
        weight = float(input(f"Enter the weight for Set {set_num} (in pounds): "))
        reps = int(input(f"Enter the number of reps for Set {set_num}: "))
        
        entry = {
            "date": date,
            "set": set_num,
            "reps": reps,
            "weight": weight
        }
        data[day][exercise].append(entry)

    print("Training data added successfully!")

def display_training_data(data):
    for day, exercises in data.items():
        print(day)
        print('-' * 40)
        for exercise, entries in exercises.items():
            print(exercise)
            print('-' * 40)
            for entry in entries:
                if 'date' in entry:
                    print("Date:", entry['date'])
                    print("Set:", entry['set'])
                    print("Reps:", entry['reps'])
                    print("Weight:", entry['weight'], "lbs")
                    print('-' * 40)
        print()

def main():
    data = load_data()
    while True:
        print("1. Add training data")
        print("2. Display training data")
        print("3. Quit")
        choice = input("Enter your choice (1-3): ")
        print()

        if choice == '1':
            add_training_data(data)
            print()
        elif choice == '2':
            display_training_data(data)
        elif choice == '3':
            save_data(data)
            print("Training data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        print()

if __name__ == '__main__':
    main()
