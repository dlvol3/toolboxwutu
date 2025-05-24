import unittest
from toolbox.model_check import check_model_ready

# 模拟一个 sklearn-like 模型类
class DummyModel:
    def __init__(self, trained=False):
        if trained:
            self.coef_ = [0.5, 0.2]  # 模拟训练后属性

# 模拟一个需要模型准备就绪才能执行的函数
@check_model_ready
def run_analysis(model):
    return "分析成功 ✅"

class TestModelCheck(unittest.TestCase):
    def test_untrained_model(self):
        model = DummyModel(trained=False)
        result = run_analysis(model)
        self.assertIsNone(result)  # 未训练模型应返回 None

    def test_trained_model(self):
        model = DummyModel(trained=True)
        result = run_analysis(model)
        self.assertEqual(result, "分析成功 ✅")

if __name__ == '__main__':
    unittest.main()
