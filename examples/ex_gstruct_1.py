# coding=utf-8

from gstruct import __version__ as gsver
from gstruct import GSBase
from gstruct import GSInterface

User = GSBase({
    "name": "Unknown",
    "sex": "intersex",
    "age": 0,
})


@User.def_method()
def greet(user):
    print("Hello, I'm {}, sex {} and age {}!".format(user.name, user.sex, user.age))


Student = GSBase({
    "User": User,
    "score": 0,
})


@Student.def_method()
def show_score(student):
    print("My name is {}, and my score is {}!".format(student.User.name, student.score))


BadStudent = GSBase({
    "Student": Student,
    "bad_score": 0,
})


@BadStudent.def_method()
def show_score(bad_student):
    print("My name is {}, and my score is always {}!".format(bad_student.Student.User.name, bad_student.bad_score))


Teacher = GSBase({
    "User": User,
    "subject": "",
})


@Teacher.def_method()
def show_subject(teacher):
    print("My name is {}, and my subject is {}!".format(teacher.User.name, teacher.subject))


@Teacher.def_method()
def teach(teacher, student):
    print("My name is {}, I'm teaching {}...".format(teacher.User.name, student.User.name))


IGreet = GSInterface(['greet'])

if __name__ == "__main__":
    print("GStruct version: {}".format(gsver))

    print("\nu:")
    u = User.new()
    u.greet()
    print(u.data)
    print()

    print("\ns:")
    s = Student.new()
    s.greet()
    s.show_score()
    print(s.data)

    print("\ns1:")
    u1 = User.new({
        "name": "Xiao Ming",
        "sex": "male",
        "age": 10,
    })
    s1 = Student.new({
        "User": u1,
        "score": 99,
    })
    if s1(IGreet):
        si = IGreet.wrap(s1)
        si.greet()
    s1.show_score()
    print(s1.data)

    print("\ns2:")
    s2 = BadStudent.new({
        "Student": s1,
    })
    s2.show_score()
    s2.Student.User.name = "Xiao Hong"
    s2.Student.User.sex = "female"
    s2.Student.User.age = 11
    print(s2.data)
    print(s1.data)  # over written!

    print("\nt1:")
    t1 = Teacher.new({
        "User": {
            "name": "Xiao Hua",
            "sex": "female",
            "age": 30,
        },
        "subject": "Math",
    })
    ti = IGreet.wrap(t1)
    ti.greet()
    # ti.teach(s1)  # raise error!
    t1.teach(s1)
    print(t1.data)
    print()

    print("\nt2:")
    t2 = Teacher.new(t1.data)  # data has been copied!
    t2.User.name = "Xiao Hei"
    print(t2.data)
    print(t1.data)  # not over written!
    print()

    print("\nt3:")
    t3 = Teacher.new({
        "User": {
            "not_exists": -1,  # auto ignore!
        }
    })
    print(t3.data)
    print()
