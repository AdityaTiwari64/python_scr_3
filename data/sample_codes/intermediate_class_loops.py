# Intermediate level - classes, loops, and conditionals
class StudentGradeBook:
    def __init__(self, student_name):
        self.name = student_name
        self.grades = []
    
    def add_grade(self, grade):
        if grade >= 0 and grade <= 100:
            self.grades.append(grade)
        else:
            print("Invalid grade! Must be between 0 and 100.")
    
    def calculate_average(self):
        if len(self.grades) == 0:
            return 0
        
        total = 0
        for grade in self.grades:
            total += grade
        
        average = total / len(self.grades)
        return average
    
    def get_letter_grade(self):
        avg = self.calculate_average()
        if avg >= 90:
            return 'A'
        elif avg >= 80:
            return 'B'
        elif avg >= 70:
            return 'C'
        elif avg >= 60:
            return 'D'
        else:
            return 'F'

# Testing the class
student = StudentGradeBook("John")
student.add_grade(85)
student.add_grade(92)
student.add_grade(78)
student.add_grade(88)

print(f"Student: {student.name}")
print(f"Average: {student.calculate_average():.1f}")
print(f"Letter Grade: {student.get_letter_grade()}")