import inspect


class Parent:
    def __init__(self) -> None:
        if inspect.getsource(Parent.my_method) != inspect.getsource(self.my_method):
            print("Child has overridden my_method.")
        else:
            print("Child has not overridden my_method.")
    def my_method(self):
        """父类中的方法，可能会在子类中被重写。"""
        print("Parent method")
    
    

class Child(Parent):
    pass
    
    # def my_method(self):
    #     """子类重写的方法。"""
    #     print("Child method")

Child()


# 继续使用前面定义的 Parent 和 Child 类

# 判断 Child 是否重写了 my_method
