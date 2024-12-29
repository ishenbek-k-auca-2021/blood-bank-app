# src/donor.py

class Donor:
    def __init__(self, name, age, blood_type):
        self.name = name
        self.age = age
        self.blood_type = blood_type

    def __str__(self):
        return f"Donor: {self.name}, Age: {self.age}, Blood Type: {self.blood_type}"

# Пример использования
if __name__ == "__main__":
    donor1 = Donor("Alice", 30, "A+")
    print(donor1)
