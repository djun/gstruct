# GStruct
## GStruct is a pythonic "struct" type framework similar to Golang struct, with self-created "interface" for it.

Usage can be realized through some code
in 'examples' directory on GitHub.

Examples on GitHub: <https://github.com/djun/gstruct/tree/master/examples>

PYPI Link: <https://pypi.org/project/GStruct/>

### GStruct 快速开始（中文版）
#### 特点简述
GStruct虽然模仿了一些Go语言的结构体（Struct）和接口（Interface）的一些形式，
但它其实是结合了Python自身的一些特色设计出来的，本意是借用Go语言的在结构体和接口上的部分设计思想，
为Python在软件工程上增添开发便利性，以及试图通过借用思想的方式实现代码质量与开发效率双提升，
并非“为了复制而复制”。

限于个人水平，GStruct目前的基本设定及实现程度大致如下：
- 尽量避免使用第三方库实现，尽可能地以更Pythonic的方式实现
- 以字典（dict）作为基本数据结构，此结构可以跟JSON、BSON等无缝对接，
且数据本身也可以作为新建GStruct对象时的传入参数
- 基本用法类似Go语言的结构体类型，可以为其定义“结构”、“方法”，可以进行组合定义，
可以通过属性访问键值和组合后的方法
- 创建GStruct对象前先定义其“类型”GSBase，淡化类型指定，定义GSBase时
只需要声明键名，及对应的默认值或被组合的GSBase对象
- 由于Python是动态语言，为GSBase定义的方法在运行时被注册，不允许反注册，
便于进行运行时的动态接口推断
- 使用GSBase创建GStruct对象时，允许往其中放入字典对象，GSBase会自动根据其定义，
对放入的字典进行键名筛选，自动创建不存在的键名及其默认值，自动忽略不需要的键名，
但对嵌入其中的GStruct对象进行GSBase“类型”推断，不符合定义的将主动报错
- 实现的“接口筛选器”GSInterface可以对GStruct对象进行方法名筛选，
包装符合要求的GStruct产生GSIWrapper对象，GSIWrapper仅允许调用筛选后的方法名
- 其他细节详见示例代码
#### 用法示例
- 引入模块
```Python
from gstruct import GSBase
from gstruct import GSInterface
```
- 定义GSBase（GStruct的基本类型）
```Python
# 简单定义
User = GSBase({
    "name": "Unknown",
    "sex": "intersex",
    "age": 0,
})

# 组合定义
Student = GSBase({
    "User": User,
    "score": 0,
})
BadStudent = GSBase({
    "Student": Student,
    "bad_score": 0,
})
Teacher = GSBase({
    "User": User,
    "subject": "",
})
```
- GSBase注册方法
```Python
# 通过def_method装饰器进行方法注册，注意这里的括号不能省略
# 括号内可以传参如“ref=True”表示调用方法时第一参数传的是GStruct的引用（默认ref=False表示仅传数据字典）
@Student.def_method()
def show_score(student):
    print("My name is {}, and my score is {}!".format(student.User.name, student.score))
@Teacher.def_method()
def teach(teacher, student):
    print("My name is {}, I'm teaching {}...".format(teacher.User.name, student.User.name))

# 组合时，可以定义同名方法，会覆盖被组合的GSBase中注册过的方法名，
# 但被组合的GSBase之间不允许重复方法名（避免方法名冲突）
@BadStudent.def_method()
def show_score(bad_student):
    print("My name is {}, and my score is always {}!".format(bad_student.Student.User.name, bad_student.bad_score))
```
- 定义GSInterface（接口筛选器）
```Python
IGreet = GSInterface(['greet'])
```
- GStruct常见用法
```Python
# 根据定义的默认值创建GStruct对象
u = User.new()
u.greet()  # 调用greet方法
print(u.data_)  # 输出GStruct包含的数据

# 传入嵌套GStruct对象的数据来创建GStruct对象
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
    # 使用GSInterface接口筛选器包装这个GStruct对象，并调用greet接口
    si = IGreet.wrap(s1)
    si.greet()
s1.show_score()

# 传入纯字典数据来创建GStruct对象
# 用协议接口实现快捷调用GSBase.new()
t1 = Teacher * {
    "User": {
        "name": "Xiao Hua",
        "sex": "female",
        "age": 30,
    },
    "subject": "Math",
}  # same as Teacher.new({ ... })
# 用协议接口实现快捷调用GSInterface.wrap()
ti = IGreet * t1  # same as IGreet.wrap(t1)
ti.greet()
# ti.teach(s1)  # raise error!
t1.teach(s1)
print(t1.data_)
```
完整示例代码请参考：<https://github.com/djun/gstruct/blob/master/examples/ex_gstruct_1.py>

### GStruct Quick Start (English ver.)
(Temporary unavailable...)

