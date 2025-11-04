"""
測試 Ray 初始化（Windows 環境）
"""
import ray
import time

# 方法 1：最小化配置
print("正在初始化 Ray (最小化配置)...")
ray.init(
    num_cpus=4,  # 根據您的 CPU 調整
    ignore_reinit_error=True,
    include_dashboard=True,  # 停用 Dashboard 和 metrics
)

print(f"Ray 版本: {ray.__version__}")
print(f"可用資源: {ray.available_resources()}")

# 測試基本功能
@ray.remote
def test_function(x):
    """測試 Ray Task"""
    return x * 2

# 測試 Task
result = ray.get(test_function.remote(21))
print(f"\n測試 Task 結果: {result} (預期: 42)")

# 測試 Actor
@ray.remote
class Counter:
    """測試 Ray Actor"""
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        return self.count

    def get_count(self):
        return self.count

# 創建並測試 Actor
counter = Counter.remote()
ray.get([counter.increment.remote() for _ in range(5)])
final_count = ray.get(counter.get_count.remote())
print(f"測試 Actor 結果: {final_count} (預期: 5)")

print("\n✅ Ray 初始化成功且功能正常！")

# 關閉 Ray
ray.shutdown()
