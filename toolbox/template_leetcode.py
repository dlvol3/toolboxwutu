import time
import logging
from pprint import pprint
from pathlib import Path

import tkinter as tk
from tkinter import messagebox, scrolledtext

# 配置 logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)


class Solution:
    def __init__(self):
        logging.info("🛠 Solution 初始化完成")
        # 初始化变量
        pass

    def __call__(self, *args, **kwargs):
        return self.solve(*args, **kwargs)

    def solve(self, nums, target):
        """
        示例逻辑：两数之和的暴力解法
        """
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []


# 示例测试用例 (输入元组, 期望输出, 描述)
test_cases = [
    (([2, 7, 11, 15], 9), [0, 1], "两数之和示例 1"),
    (([3, 2, 4], 6), [1, 2], "两数之和示例 2"),
    (([3, 3], 6), [0, 1], "两数之和示例 3"),
]

# 执行测试并生成结构化结果
s = Solution()
results = []

for i, (input_data, expected, desc) in enumerate(test_cases, 1):
    print(f"\n🧪 测试用例 {i} - {desc}")
    pprint({"输入": input_data})

    start = time.time()
    try:
        result = s(*input_data)
    except Exception as e:
        result = f"❌ 报错: {e}"
    end = time.time()

    correct = result == expected
    test_summary = {
        "输出": result,
        "期望": expected,
        "是否正确": "✅ 正确" if correct else "❌ 错误",
        "耗时 (ms)": round((end - start) * 1000, 2),
    }

    pprint(test_summary)
    results.append({"测试编号": i, "描述": desc, "输入": input_data, **test_summary})

# 生成 Markdown 报告
md_lines = ["# 测试报告\n"]
for r in results:
    md_lines.append(f"## 测试用例 {r['测试编号']} - {r['描述']}")
    md_lines.append(f"- 输入: `{r['输入']}`")
    md_lines.append(f"- 输出: `{r['输出']}`")
    md_lines.append(f"- 期望: `{r['期望']}`")
    md_lines.append(f"- 是否正确: {r['是否正确']}")
    md_lines.append(f"- 耗时: {r['耗时 (ms)']} ms\n")

report_path = Path("test_report.md")
report_path.write_text("\n".join(md_lines), encoding="utf-8")
logging.info(f"📄 已生成 Markdown 报告: {report_path.resolve()}")


# 简易 GUI（按钮触发查看报告）
def show_report():
    with open("test_report.md", encoding="utf-8") as f:
        content = f.read()
    popup = tk.Tk()
    popup.title("测试报告预览")
    text_area = scrolledtext.ScrolledText(popup, wrap=tk.WORD, width=100, height=30)
    text_area.insert(tk.INSERT, content)
    text_area.pack(padx=10, pady=10)
    popup.mainloop()


# 创建主窗口带按钮
def launch_gui():
    root = tk.Tk()
    root.title("LeetCode 测试器")

    btn = tk.Button(
        root,
        text="📄 打开 Markdown 报告",
        command=show_report,
        font=("Arial", 14),
        bg="#4CAF50",
        fg="white",
        padx=10,
        pady=5,
    )
    btn.pack(padx=20, pady=20)

    root.mainloop()


launch_gui()
