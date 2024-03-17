class MyClass:
    def method(self):
        return "原始方法"
    
    @property
    def value(self):
        return 1

def new_method(self):
    return "new method"


# 使用types.MethodType
import types

# 重新创建一个实例
obj2 = MyClass()

# 只修改obj2的method方法，不影响类或其他实例
print(isinstance(obj2.__class__.value, property))
setattr(obj2, "method", new_method)
#obj2.method = types.MethodType(new_method, obj2)
print(obj2.method())  # 输出: 新方法

obj3= MyClass()
print(obj3.method())  # 输出: 新方法