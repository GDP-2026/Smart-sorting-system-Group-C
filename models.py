class Person:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = int(age)
        self.grade = float(grade)

    def __repr__(self):
        return f"{self.name} (Age: {self.age}, Grade: {self.grade})"