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
          overall_student_rating += average_student_score / len(listener.grades[course])
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

best_student1 = Student('Антон', 'Антонов', 'Мужской')
best_student1.courses_in_progress += ['Git', 'Python']
best_student1.finished_courses += ['Введение в программирование']

best_student2 = Student('Михаил', 'Михайлов', 'Мужской')
best_student2.courses_in_progress += ['Git', 'Python']
best_student2.finished_courses += ['Введение в программирование']

cool_reviewer1 = Reviewer('Ктото', 'Ктотов')
cool_reviewer1.courses_attached += ['Python']

cool_reviewer2 = Reviewer('Кто-то еще', 'Кто-то еще')
cool_reviewer2.courses_attached += ['Python']

cool_lecturer1 = Lecturer('Аркадий', 'Иванов')
cool_lecturer1.courses_mentored += ['Git']

cool_lecturer2 = Lecturer('Игорь', 'Игорев')
cool_lecturer2.courses_mentored += ['Python']

cool_reviewer1.rate_hw(best_student1, 'Python', 10)
cool_reviewer1.rate_hw(best_student1, 'Python', 9)
cool_reviewer1.rate_hw(best_student1, 'Python', 10)

cool_reviewer2.rate_hw(best_student2, 'Python', 8)
cool_reviewer2.rate_hw(best_student2, 'Python', 7)
cool_reviewer2.rate_hw(best_student2, 'Python', 9)

best_student1.rate_lecture(cool_lecturer1, 'Git', 9)
best_student1.rate_lecture(cool_lecturer1, 'Git', 10)
best_student1.rate_lecture(cool_lecturer1, 'Python', 7)

best_student2.rate_lecture(cool_lecturer2, 'Python', 8)
best_student2.rate_lecture(cool_lecturer2, 'Python', 9)
best_student2.rate_lecture(cool_lecturer2, 'Python', 10)

print(best_student1)
print(best_student2)

print(cool_lecturer1)
print(cool_lecturer2)

print(cool_reviewer1)
print(cool_reviewer2)

print(f'{best_student1.name} учится лучше чем {best_student2.name}' if best_student1 > best_student2 else
    f'{best_student2.name} учится лучше чем {best_student1.name}')

print(f'{cool_lecturer1.name} преподает лучше чем {cool_lecturer2.name}' if cool_lecturer1 > cool_lecturer2 else
    f'{cool_lecturer2.name} преподает лучше чем {cool_lecturer1.name}')

print(f'Средняя оценка студентов по курсу "Git": {grades_students([best_student1, best_student2], "Git")}')
print(f'Средняя оценка студентов по курсу "Python": {grades_students([best_student1, best_student2], "Python")}')

print(f'Средняя оценка лекторов по курсу "Git": {grades_lecturers([cool_lecturer1, cool_lecturer2], "Git")}')
print(f'Средняя оценка лекторов по курсу "Python": {grades_lecturers([cool_lecturer1, cool_lecturer2], "Python")}')
