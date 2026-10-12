# 项目维护工具

[项目首页](../README.md) · [服务器教程](../docs/SERVER_GUIDE.md)

| 用途 | 命令 |
|---|---|
| 查看服务器练习配置 | `python3 scripts/server_checkout.py list` |
| 选择练习，仅在服务器最小检出目录使用 | `python3 scripts/server_checkout.py set week1` |
| 检查文档链接、Notebook JSON 与工具语法 | `python3 scripts/check_structure.py` |
| 验证回归与基础示例 | `.venv/bin/python scripts/verify_week1.py` |
| 验证分类、NumPy/PyTorch 带练 | `.venv/bin/python scripts/verify_bootcamp.py` |
| 工具的离线回归测试 | `python3 -m unittest discover -s scripts/tests -v` |

从项目根目录执行。示例验证输出在被 Git 忽略的 `outputs/`，不改写参考 Notebook。根目录 pytest 只收集工具测试；学校模板中的测试在对应个人任务目录执行。

旧的批量资料下载、Release 归档和整门课同步工具已删除。新增公开 GitHub 练习片段时，保留来源与许可，先验证小数据、依赖与运行结果，再纳入课程。
