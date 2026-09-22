# 数据来源与使用约定

来源：Cortez, P. (2008). Student Performance [Dataset]. UCI Machine Learning Repository.
DOI: https://doi.org/10.24432/C5TG7T
页面：https://archive.ics.uci.edu/dataset/320/student+performance
下载：https://archive.ics.uci.edu/static/public/320/student+performance.zip
获取日期：2026-09-21。页面声明许可为 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。

`raw/student-mat.csv` 是下载包内数学课程原始文件，395 行、33 列，分号分隔，未改动。
`raw/student.txt` 是随包提供的字段说明。未混入葡萄牙语课程，避免同一学生跨科重复。
SHA-256：`e47f9ee225e1ee6e69b7564e6dac7123e80b8486677fe111f351964cef5dec80`。

本教材使用的 G1/G2/G3 为三个阶段成绩（0～20）；studytime 为时间档位，failures 为既往不及格次数编码。完整定义以原始说明为准。
不要把档位当小时、把成绩当 100 分制、把 G3=0 当缺失。

原始数据不缺失。第三天对训练集 12 行副本人工注入缺失值、非法文本、非法目标、空格、重复记录；只用于教学。教学副本不是新的真实观测。
所有导出到 `course/bootcamp/week1/outputs/` 的 CSV/PNG 都是课程派生结果，原始文件始终保留。
