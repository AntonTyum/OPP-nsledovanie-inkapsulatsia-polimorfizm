class Student:
  def __init__(self, name, surname, gender):
      self.name = name
      self.surname = surname
      self.gender = gender
      self.finished_courses = []
      self.courses_in_progress = []
      self.grades = {}

  def rate_lecture(self, lecturer, course, grade):
      if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_mentored:
          if course in lecturer.grades:
              lecturer.grades[course] += [grade]
          else:
              lecturer.grades[course] = [grade]
      else:
          return 'Ошибка'

  def __str__(self):
      average_grade = sum(sum(grades) / len(grades) for grades in self.grades.values()) / len(
          self.grades) if self.grades else 0
      courses_in_progress_str = ', '.join(self.courses_in_progress)
      finished_courses_str = ', '.join(self.finished_courses)
      return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {average_grade:.1f}\n" \
             f"Курсы в процессе изучения: {courses_in_progress_str}\nЗавершенные курсы: {finished_courses_str}"

  def __lt__(self, student):
      if not isinstance(student, Student):
          print(f'Такого студента нет')
          return
      return self.calculate_average_grade() < student.calculate_average_grade()

  def calculate_average_grade(self):
      return sum(sum(grades) / len(grades) for grades in self.grades.values()) / len(
          self.grades) if self.grades else 0


class Mentor:
  def __init__(self, name, surname):
      self.name = name
      self.surname = surname
      self.courses_attached = []


class Lecturer(Mentor):
  def __init__(self, name, surname):
      super().__init__(name, surname)
      self.courses_mentored = []
      self.grades = {}

  def __str__(self):
      average_grade = sum(sum(grades) / len(grades) for grades in self.grades.values()) / len(
          self.grades) if self.grades else 0
      return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {average_grade:.1f}"

  def __lt__(self, other):
      return self.calculate_average_grade() < other.calculate_average_grade()

  def calculate_average_grade(self):
      return sum(sum(grades) / len(grades) for grades in self.grades.values()) / len(
          self.grades) if self.grades else 0

  def rate_hw(self, student, course, grade):
      if isinstance(student, Student) and course in self.courses_mentored and course in student.courses_in_progress:
          if course in student.grades:
              student.grades[course] += [grade]
          else:
              student.grades[course] = [grade]
      else:
          return 'Ошибка'


class Reviewer(Mentor):
  def rate_hw(self, student, course, grade):
      if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
          if course in student.grades:
              student.grades[course] += [grade]
          else:
              student.grades[course] = [grade]
      else:
          return 'Ошибка'

  def __str__(self):
      return f"Имя: {self.name}\nФамилия: {self.surname}\nУ лекторов:"


def grades_students(students_list, course):
  overall_student_rating = 0
  lectors = 0
  for listener in students_list:
      if course in listener.grades.keys():
          average_student_score = 0
          for grades in listener.grades[course]:
              average_student_score += grades
          overall_student_rating = average_student_score / len(listener.grades[course])
          average_student_score += overall_student_rating
          lectors += 1
  if overall_student_rating == 0:
      return f'Оценок по этому предмету нет'
  else:
      return f'{overall_student_rating / lectors:.2f}'


def grades_lecturers(lecturer_list, course):
  average_rating = 0
  b = 0
  for lecturer in lecturer_list:
      if course in lecturer.grades.keys():
          lecturer_average_rates = 0
          for rate in lecturer.grades[course]:
              lecturer_average_rates += rate
          overall_lecturer_average_rates = lecturer_average_rates / len(lecturer.grades[course])
          average_rating += overall_lecturer_average_rates
          b += 1
  if average_rating == 0:
      return f'Оценок по этому предмету нет'
  else:
      return f'{average_rating / b:.2f}'


best_student = Student('Антон', 'Антонов', 'Мужской')
best_student.courses_in_progress += ['Git', 'Python']
best_student.finished_courses += ['Введение в программирование']

cool_reviewer = Reviewer('Ктото', 'Ктотов')
cool_reviewer.courses_attached += ['Python']

cool_reviewer.rate_hw(best_student, 'Python', 10)
cool_reviewer.rate_hw(best_student, 'Python', 9)
cool_reviewer.rate_hw(best_student, 'Python', 10)

print(best_student)

best_lecturer = Lecturer('Аркадий', 'Иванов')
best_lecturer.courses_mentored += ['Git']

best_student.rate_lecture(best_lecturer, 'Git', 9)
best_student.rate_lecture(best_lecturer, 'Git', 10)
best_student.rate_lecture(best_lecturer, 'Python', 7)

print(best_lecturer)

another_student = Student('Василий', 'Васильев', 'Мужской')
another_student.courses_in_progress += ['Git', 'Python']
cool_lecturer2 = Lecturer('Игорь', 'Игорев')
cool_lecturer2.courses_mentored += ['Python']
cool_lecturer2.rate_hw(another_student, 'Python', 8)

print(best_student > another_student)
print(best_lecturer > cool_lecturer2)

print(f'Средняя оценка студентов по курсу "Git": {grades_students([best_student, another_student], "Git")}')
print(f'Средняя оценка студентов по курсу "Python": {grades_students([best_student, another_student], "Python")}')

print(f'Средняя оценка лекторов по курсу "Git": {grades_lecturers([best_lecturer, cool_lecturer2], "Git")}')
print(f'Средняя оценка лекторов по курсу "Python": {grades_lecturers([best_lecturer, cool_lecturer2], "Python")}')
