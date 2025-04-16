class Student:
    def __init__(self, name, age, grades):
        self.name = name
        self.age = age
        self.grades = grades

    def get_average(self):
        return sum(self.grades) / len(self.grades)

    def __str__(self):
        return f'Student: {self.name}, Age: {self.age}, Average Grade: {self.get_average():.2f}'


class Teacher:
    def __init__(self, name):
        self.name = name
        self.students = []

    def add_student(self, students):
        if isinstance(students, list):  # Nếu là danh sách
            for std in students: # 
                if isinstance(std, Student):
                    self.students.append(std)
        elif isinstance(students, Student):  # Nếu không phải danh sách
            self.students.append(students)

    def print_students(self):
        return "\n".join(str(std) for std in self.students) # In danh sách học sinh
    def get_average(self):
        if not self.students:
            return 0  # Tránh trường hợp chia cho 0
        return sum(std.get_average() for std in self.students) / len(self.students)

    def __str__(self):
        return f'Danh sách sinh viên do giảng viên {self.name} quản lý:\n{self.print_students()}\n' \
               f'Điểm trung bình của lớp: {self.get_average():.2f}'


# Tạo đối tượng giáo viên
teacher1 = Teacher('Nguyen Van A')
teacher2 = Teacher('Tran Van B')

# Tạo đối tượng học sinh
std1 = Student('Nguyen Van B', 20, [8, 7, 8])
std2 = Student('Nguyen Van C', 19, [6, 2, 1])
std3 = Student('Nguyen Van D', 18, [3, 5, 9])
std4 = Student('Nguyen Van E', 21, [5, 3, 9])
std5 = Student('Nguyen Van F', 22, [2, 6, 0])

# Danh sách học sinh cho từng giáo viên
students_1 = [std1, std2, std3]
students_2 = [std4, std5]

# Thêm học sinh vào giáo viên
teacher1.add_student(students_1)
teacher2.add_student(students_2)

# In thông tin giáo viên
print(teacher1)
print()
print(teacher2)
