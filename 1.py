def single01(cls):  
    s=[]  #这里定义了一个私有列表，也可以声明一个变量，在wrap用关键字nonlocal去调用
    def wrap(*args,**kwargs):  
        if not s:  
            s.append(cls(*args,**kwargs))  
        return s  
    return wrap  
 
@single01  
class A(object):  
    def __init__(self,name):  
        self.name = name


a = A("tmac")
b = A("kobe")
print(a is b)
print(a)#列表
print(b)