import os
import shutil
import re
from PIL import Image
import argparse


def main():
    parser = argparse.ArgumentParser(description='分类图片到横、竖、正方形目录，并重命名为0001、0002等格式。')
    parser.add_argument('--input', default='test/images', help='输入目录，默认为 test/images')
    parser.add_argument('--output', default='test/sorted_images', help='输出根目录，默认为 test/sorted_images')
    parser.add_argument('--copy', action='store_true', help='使用复制而非移动文件')
    parser.add_argument('--allow_error', action='store_true', help='启用5%%误差的正方形判断（当宽高比≤1.05时视为正方形）')
    # 新增重命名参数
    parser.add_argument('--rename', action='store_true', help='启用四位数字序列重命名（默认保留原始文件名）')
    args = parser.parse_args()

    input_dir = args.input
    output_root = args.output
    use_copy = args.copy
    allow_error = args.allow_error
    enable_rename = args.rename  # 新增参数读取

    categories = ['横向', '纵向', '正方形']
    for cat in categories:
        os.makedirs(os.path.join(output_root, cat), exist_ok=True)

    file_pattern = re.compile(r'^(\d{4})(\..+)?$')

    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if not os.path.isfile(filepath):
            continue

        try:
            with Image.open(filepath) as img:
                width, height = img.size
        except Exception as e:
            print(f"无法处理文件 {filename}，错误：{e}，跳过。")
            continue

        # 分类判断逻辑保持不变...
        if allow_error:
            if width == 0 or height == 0:
                category = '正方形'
            else:
                max_dim = max(width, height)
                min_dim = min(width, height)
                ratio = max_dim / min_dim
                category = '正方形' if ratio <= 1.05 else ('横向' if width > height else '纵向')
        else:
            if width > height:
                category = '横向'
            elif height > width:
                category = '纵向'
            else:
                category = '正方形'

        target_dir = os.path.join(output_root, category)

        if enable_rename:
            # 生成序列号
            max_num = 0
            for existing_file in os.listdir(target_dir):
                match = file_pattern.match(existing_file)
                if match:
                    current_num = int(match.group(1))
                    max_num = max(max_num, current_num)
            new_num = max_num + 1

            # 构造新文件名
            _, ext = os.path.splitext(filename)
            ext_part = ext.lower().lstrip('.')
            new_filename = f"{new_num:04d}.{ext_part}" if ext_part else f"{new_num:04d}"
        else:
            new_filename = filename  # 直接使用原始文件名

        target_path = os.path.join(target_dir, new_filename)

        # 执行文件操作
        try:
            if use_copy:
                shutil.copy2(filepath, target_path)
                print(f"已复制 {filename} 到 {target_path}")
            else:
                shutil.move(filepath, target_path)
                print(f"已移动 {filename} 到 {target_path}")
        except Exception as e:
            print(f"操作失败：{e}")


if __name__ == "__main__":
    main()
