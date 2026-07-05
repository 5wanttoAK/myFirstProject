from pathlib import Path
import re
import openpyxl


def getLoad(path):
    return path.replace('\\', '/')


# 提示用户输入文件夹路径
load = input("请输入包含作业的文件夹路径: ").strip()

# 去除可能存在的双引号
load = load.strip('"').strip("'")

# 检查路径是否为空
if not load:
    print("错误：路径不能为空！")
    exit(1)

folder = Path(getLoad(load))

# 检查路径是否存在
if not folder.exists():
    print(f"错误：路径 '{load}' 不存在！")
    exit(1)

# 检查是否为目录
if not folder.is_dir():
    print(f"错误：'{load}' 不是一个有效的文件夹路径！")
    exit(1)

# 提示用户输入Excel文件路径
excel_path = input("请输入学生信息Excel文件路径: ").strip()

# 去除可能存在的双引号
excel_path = excel_path.strip('"').strip("'")

# 检查Excel文件路径
if not excel_path:
    print("错误：Excel文件路径不能为空！")
    exit(1)

excel_file = Path(getLoad(excel_path))

if not excel_file.exists():
    print(f"错误：Excel文件 '{excel_path}' 不存在！")
    exit(1)

if not excel_file.is_file():
    print(f"错误：'{excel_path}' 不是一个有效的文件路径！")
    exit(1)

# 读取Excel文件，获取所有学生信息
wb = openpyxl.load_workbook(str(excel_file))
ws = wb.active

# 假设第一行是表头，从第二行开始读取数据
# 假设学号在第一列，姓名在第二列（可根据实际情况调整）
all_students = {}  # {学号: 姓名}

for row in ws.iter_rows(min_row=2, values_only=True):
    if row[0] is not None:  # 确保学号不为空
        student_id = str(row[0]).strip()
        student_name = str(row[1]).strip() if row[1] else ""
        # 提取纯数字的学号（去除可能的空格或其他字符）
        id_match = re.search(r'\d+', student_id)
        if id_match:
            clean_id = id_match.group()
            all_students[clean_id] = student_name

print(f"共读取到 {len(all_students)} 个学生信息")

# 从文件夹中提取已提交作业的学生学号
submitted_ids = set()

for item in folder.iterdir():
    if item.is_file():
        # 匹配文件名中的12位学号
        match = re.search(r'\d{12}', item.name)
        if match:
            submitted_ids.add(match.group())

print(f"共找到 {len(submitted_ids)} 个已提交的作业")

# 找出未交作业的学生
missing_students = []
for student_id, student_name in all_students.items():
    if student_id not in submitted_ids:
        missing_students.append((student_id, student_name))

# 按学号升序排序
missing_students.sort(key=lambda x: x[0])

# 输出结果
print("\n" + "=" * 50)
print("未交作业的学生名单：")
print("=" * 50)

if missing_students:
    for student_id, student_name in missing_students:
        print(f"学号：{student_id}  姓名：{student_name}")
    print(f"\n共 {len(missing_students)} 个学生未交作业")
else:
    print("所有学生都已提交作业！")

input("按 Enter 键退出...")
