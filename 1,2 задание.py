class Student:
  def __init__(self, name, surname, gender):
      self.name = name
      self.surname = surname
      self.gender = gender
      self.finished_courses = []
      self.courses_in_progress = []
      self.grades = {}

  def rate_lecture(self, lecturer, course, grade):
      if isinstance(lecturer, Lecturer) and course in self.courses_in_progress \
              and course in lecturer.courses_mentored:
          if course in lecturer.grades:
              lecturer.grades[course] += [grade]
          else:
              lecturer.grades[course] = [grade]
      else:
          return 'Ошибка'


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


class Reviewer(Mentor):
  def rate_hw(self, student, course, grade):
      if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
          if course in student.grades:
              student.grades[course] += [grade]
          else:
              student.grades[course] = [grade]
      else:
          return 'Ошибка'


best_student = Student('Антон', 'Антонов', 'Мужской')
best_student.courses_in_progress += ['Git', 'Python']

cool_reviewer = Reviewer('Ктото', 'Ктотов')
cool_reviewer.courses_attached += ['Python']

cool_reviewer.rate_hw(best_student, 'Python', 10)
cool_reviewer.rate_hw(best_student, 'Python', 9)
cool_reviewer.rate_hw(best_student, 'Python', 10)

print(best_student.grades)

best_lecturer = Lecturer('Аркадий', 'Иванов')
best_lecturer.courses_mentored += ['Git']

best_student.rate_lecture(best_lecturer, 'Git', 9)
best_student.rate_lecture(best_lecturer, 'Git', 10)
best_student.rate_lecture(best_lecturer, 'Python', 7)

print(best_lecturer.grades)