GStruct
=======

GStruct is a pythonic "struct" type framework similar to Golang struct, with self-created "interface" for it.
-------------------------------------------------------------------------------------------------------------

Usage can be realized through some code in 'examples' directory on
GitHub.

Examples on GitHub: https://github.com/djun/gstruct/tree/master/examples

GStruct ���ٿ�ʼ�����İ棩
~~~~~~~~~~~~~~~~~~~~~~~~~~

�ص����
^^^^^^^^

GStruct��Ȼģ����һЩGo���ԵĽṹ�壨Struct���ͽӿڣ�Interface����һЩ��ʽ��
������ʵ�ǽ����Python�����һЩ��ɫ��Ƴ����ģ������ǽ���Go���Ե��ڽṹ��ͽӿ��ϵĲ������˼�룬
ΪPython����������������������ԣ��Լ���ͼͨ������˼��ķ�ʽʵ�ִ��������뿪��Ч��˫������
���ǡ�Ϊ�˸��ƶ����ơ���

���ڸ���ˮƽ��GStructĿǰ�Ļ����趨��ʵ�̶ֳȴ������£� -
��������ʹ�õ�������ʵ�֣������ܵ��Ը�Pythonic�ķ�ʽʵ�� -
���ֵ䣨dict����Ϊ�������ݽṹ���˽ṹ���Ը�JSON��BSON���޷�Խӣ�
�����ݱ���Ҳ������Ϊ�½�GStruct����ʱ�Ĵ������ -
�����÷�����Go���ԵĽṹ�����ͣ�����Ϊ�䶨�塰�ṹ�����������������Խ�����϶��壬
����ͨ�����Է��ʼ�ֵ����Ϻ�ķ��� -
����GStruct����ǰ�ȶ����䡰���͡�GSBase����������ָ��������GSBaseʱ
ֻ��Ҫ��������������Ӧ��Ĭ��ֵ����ϵ�GSBase���� -
����Python�Ƕ�̬���ԣ�ΪGSBase����ķ���������ʱ��ע�ᣬ������ע�ᣬ
���ڽ�������ʱ�Ķ�̬�ӿ��ƶ� -
ʹ��GSBase����GStruct����ʱ�����������з����ֵ����GSBase���Զ������䶨�壬
�Է�����ֵ���м���ɸѡ���Զ����������ڵļ�������Ĭ��ֵ���Զ����Բ���Ҫ�ļ�����
����Ƕ�����е�GStruct�������GSBase�����͡��ƶϣ������϶���Ľ��������� -
ʵ�ֵġ��ӿ�ɸѡ����GSInterface���Զ�GStruct������з�����ɸѡ��
��װ����Ҫ���GStruct����GSIWrapper����GSIWrapper���������ɸѡ��ķ�����
- ����ϸ�����ʾ������ #### �÷�ʾ�� - ����ģ��

.. code:: Python

    from gstruct import GSBase
    from gstruct import GSInterface

-  ����GSBase��GStruct�Ļ������ͣ� \`\`\`Python # �򵥶��� User =
   GSBase({ "name": "Unknown", "sex": "intersex", "age": 0, })

��϶���
========

Student = GSBase({ "User": User, "score": 0, }) BadStudent = GSBase({
"Student": Student, "bad\_score": 0, }) Teacher = GSBase({ "User": User,
"subject": "", }) ``- GSBaseע�᷽��``\ Python #
ͨ��def\_methodװ�������з���ע�ᣬע����������Ų���ʡ�� #
�����ڿ��Դ����硰ref=True����ʾ���÷���ʱ��һ����������GStruct�����ã�Ĭ��ref=False��ʾ���������ֵ䣩
@Student.def\_method() def show\_score(student): print("My name is {},
and my score is {}!".format(student.User.name, student.score))
@Teacher.def\_method() def teach(teacher, student): print("My name is
{}, I'm teaching {}...".format(teacher.User.name, student.User.name))

���ʱ�����Զ���ͬ���������Ḳ�Ǳ���ϵ�GSBase��ע����ķ�������
================================================================

������ϵ�GSBase֮�䲻�����ظ������������ⷽ������ͻ��
======================================================

@BadStudent.def\_method() def show\_score(bad\_student): print("My name
is {}, and my score is always
{}!".format(bad\_student.Student.User.name, bad\_student.bad\_score))
``- ����GSInterface���ӿ�ɸѡ����``\ Python IGreet =
GSInterface(['greet']) ``- GStruct�����÷�``\ Python #
���ݶ����Ĭ��ֵ����GStruct���� u = User.new() u.greet() # ����greet����
print(u.data\_) # ���GStruct����������

����Ƕ��GStruct���������������GStruct����
==========================================

u1 = User.new({ "name": "Xiao Ming", "sex": "male", "age": 10, }) s1 =
Student.new({ "User": u1, "score": 99, }) if s1(IGreet): #
ʹ��GSInterface�ӿ�ɸѡ����װ���GStruct���󣬲�����greet�ӿ� si =
IGreet.wrap(s1) si.greet() s1.show\_score()

���봿�ֵ�����������GStruct����
===============================

��Э��ӿ�ʵ�ֿ�ݵ���GSBase.new()
==================================

t1 = Teacher \* { "User": { "name": "Xiao Hua", "sex": "female", "age":
30, }, "subject": "Math", } # same as Teacher.new({ ... }) #
��Э��ӿ�ʵ�ֿ�ݵ���GSInterface.wrap() ti = IGreet \* t1 # same as
IGreet.wrap(t1) ti.greet() # ti.teach(s1) # raise error! t1.teach(s1)
print(t1.data\_) \`\`\`
����ʾ��������ο���\ https://github.com/djun/gstruct/blob/master/examples/ex_gstruct_1.py

# GStruct Quick Start (English ver.)  (Temporary unavailable...)
