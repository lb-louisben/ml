# 资料与导航校验

2026-09-21 完成。

- 官方原件：415 个，387 份 PDF、28 个 ZIP；原件约 1374.4 MiB。
- 所有文件 SHA256 与 library/manifest.json 一致。
- 387 份 PDF 经 pdfinfo 解析成功，文件头与 EOF 检查通过。
- 28 个 ZIP 通过目录解析和 testzip CRC 完整性检查。
- 11 个作业发布包已解压，资料库含解压副本约 2.1 GB。
- 57 个本项目与生成导航 Markdown 文件检查通过，本地链接与使用的锚点均存在。上游原件中的联网链接未改写。
- git diff --check 通过。

官方失效项：CS182 HW2 仓库、CS231n 2025 handouts/derivatives.pdf 与 handouts/linear-backprop.pdf 返回 404。目录提供对应的 CNN 作业、导数与反传资料替代入口。

版本差异：CS231n 2025 作业网页目前指向 2026 ZIP，已在课程目录和学习指南标明。CS224N 2025 页面复用部分旧年份 notes，保留原名和年份。

校验范围是下载完整性、PDF 可解析性和本地导航；尚未安装、执行或训练新增官方作业。第一周 Notebook 的数据路径保持原样，原有学习记录未修改。

## 作业隔离与完整 GitHub 存储（2026-10-12）

- Bootcamp、中文补充作业及 NJU A0～A5 已独立到 `assignments/`，个人 A0 实现完整保存在 `work/nju-llm-2026/a0/`。130 份 NJU 原始分支文件的 SHA256 全部匹配来源清单。
- 搬移后完整执行 Week 1 的 10 本及 Week 2/3 的 3 本 Notebook，13/13 通过；源文件原有输出与元数据保留。
- 维护工具的 39 项离线测试通过；完整结构检查覆盖 79 份文档、17 本个人与教学 Notebook、18 份 Python 文件，0 个错误。GitHub 自动结构检查与回归测试通过。
- 已从 GitHub 实际执行 partial clone 和 NJU A0 检出：34 份工作文件约 391 KiB，Git 对象包约 111 KiB，工作树干净；未检出 `course/`、`library/` 或个人课程讲义。Week 1 + A01 组合及全部练习范围的切换也通过。
- [公开资料快照 materials-2026-10-12](https://github.com/lb-louisben/ml/releases/tag/materials-2026-10-12) 已发布：37 个附件，共 1,396,622,611 字节。28 个原始 ZIP 独立下载，其余资料按课程打包，来源与归档清单一并保存；全部远端附件的大小、状态与 SHA256 已核对。
- 归档覆盖 573 份文件，包含全部 415 份成功下载原件。737 个解压副本与原始 ZIP 一致，解压副本可重建；环境、模型权重、缓存与运行产物不上传。
- 从公开 Release 实际下载 CS224N A1：只取得一个作业 ZIP，没有取得讲义或其他课程材料，SHA256 通过。
- 在空的临时目录从 Release 恢复 MIT 18.06SC，279 份原件、网页与来源清单逐份核对大小和 SHA256，全部通过。

使用方法见 [服务器教程](SERVER_GUIDE.md) 与 [GitHub 存储方案](GITHUB_STORAGE.md)。这些检查证明目录、下载完整性与已选演示可运行，不代表个人作业已完成或新增海外课程代码已执行。
