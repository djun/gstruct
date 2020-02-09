# GStruct
## GStruct is a pythonic "struct" type framework similar to Golang struct, with self-created "interface" for it.

Usage can be realized through some code
in 'examples' directory on GitHub.

Examples on GitHub: <https://github.com/djun/gstruct/tree/master/examples>

### GStruct 快速开始（中文版）
#### 特点简述
GStruct虽然模仿了一些Go语言的结构体（Struct）和接口（Interface）的一些形式，
但它其实是结合了Python自身的一些特色设计出来的，本意是借用Go语言的在结构体和接口上的部分设计思想，
为Python在软件工程上增添开发便利性，以及试图通过借用思想的方式实现代码质量与开发效率双提升，
而不是“为了复制而复制”。

限于个人水平，GStruct目前的基本设定及实现程度大致如下：
1. 尽量避免使用第三方库实现，尽可能地以Pythonic的方式实现；
2. 以字典（dict）作为基本数据结构，可以为其定义“结构”、“方法”，可以进行组合定义，
可以通过属性访问键值和组合后的方法，基本用法类似Go语言的结构体类型；
3. 由于Python是动态语言，且原本的设计是淡化变量的类型指定的，故创建GStruct的“类型”GSBase时，
设定为只需要声明键名及对应的默认值或被组合的GSBase对象，其方法也在运行时被注册；
4. GSBase对象可以接受包含或不包含GStruct对象的字典进行实例化，
内部会自动根据GStruct对应的GSBase定义，对传入的字典进行键名筛选，
如果字典包含的GStruct对象的定义不与GSBase中的定义相匹配，则会主动报错，
如用字典代替GStruct对象则会自动忽略不匹配的键名，如键名不存在则根据默认值自动创建；
5. 实现的“接口筛选器”GSInterface可以提供方法名筛选，
其可以对符合要求的GStruct对象进行包装产生GSIWrapper对象，有类似“断言”的效果；
6. GStruct对象可以动态推断是否与另一GStruct、GSBase或GSInterface对象相匹配；
7. 其他细节详见示例代码；
#### 用法示例
(TODO)

### GStruct Quick Start (English ver.)
(Temporary unavailable...)

