

import os
import json



from pydantic import validate_call,BaseModel
from typing_extensions import Literal




@validate_call
def select_object(type:Literal['all_roles',#分为两个阶段，准备阶段和使用阶段，询问选择对象为准备阶段，会返回一个function，调用这个function为使用阶段
                               'opponent_roles', #只有在creature的战吼，sorcery的打出的能力，和instant 打出能力时，会用到
                               'your_roles',
                               'all_creatures',
                               'opponent_creatures',
                               'your_creatures',
                               'all_lands',
                               'opponent_lands',
                               'your_lands',
                               ''],
                  number:int):
    
    
    key_word="selected_object"

    def new_decorator(func):
        def new_func(self,*args, **kwargs):
            objects= ()
            print(objects)
            kwargs[key_word] = objects
            def prepared_function():
                func(self,*args,**kwargs)
            return prepared_function
        return new_func
    return new_decorator


class A:
    @select_object("",1)
    def a(self,b=None,selected_object=()):
        pass

class B(A):
    pass

a=B()
r=a.a(1)
r()