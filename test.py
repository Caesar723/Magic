import time
time.sleep(1) 
# 开始计时
start_time = time.perf_counter()
print(start_time)
print(start_time)
# 执行一些代码
# 例如，模拟一段代码的运行，这里我们简单地使用 sleep 来模拟
time.sleep(1) # 模拟代码运行，暂停2秒

# 结束计时
end_time = time.perf_counter()

# 计算并打印执行时间
print(f"代码执行时间：{end_time - start_time}秒")
