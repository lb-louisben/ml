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
