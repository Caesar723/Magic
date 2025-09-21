import builtins
import inspect

original_print = builtins.print
def custom_print(*args, **kwargs):
    # 获取调用该函数的帧记录
    frame = inspect.currentframe().f_back
    # 获取文件名
    filename = frame.f_code.co_filename
    # 获取行号
    lineno = frame.f_lineno
    
    # 调用原生的 print 函数
    original_print(f'{filename}:{lineno}:', *args, **kwargs,flush=True)

# 重写 print 函数
builtins.print = custom_print
