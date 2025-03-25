# 图片分类整理工具

本工具用于自动将图片按宽高比分类到`横向`、`纵向`、`正方形`三个目录，支持灵活的文件操作和误差判断。

## 📋 1. 功能特性
- **智能分类**：严格模式 vs 5%误差模式
- **文件操作**：移动/复制可选
- **命名策略**：保留原名或四位数字序列
- **安全处理**：自动创建目录，异常捕获

## ⚙️ 2. 环境配置（推荐使用Conda）
```bash
# 创建并激活conda环境
conda create -n img-sorter python=3.8
conda activate img-sorter
```
```bash
# 安装依赖
pip install -r requirements.txt
```

## 🚀 3. 快速开始

### 基本用法
```bash
python main.py
```
默认行为：
- 从 test/images 读取图片
- 输出到 test/sorted_images
- 移动文件并严格判断宽高比

### 获取命令行帮助
```bash
python main.py -h
```

### 完整参数
| 参数              | 说明                             |
|-----------------|--------------------------------|
| `--input`       | 输入目录（默认：`test/images`）         |
| `--output`      | 输出根目录（默认：`test/sorted_images`） |
| `--copy`        | 启用复制模式（默认移动文件）                 |
| `--allow_error` | 启用5%宽高比误差的正方形判断                |
| `--rename`      | 启用四位数字序列重命名                    |
## 🚀 4. 使用示例

### 启用误差判断 + 重命名
```bash
python main.py --allow_error --rename
```
### 自定义路径 + 复制模式
```bash
python main.py --input ~/photos --output ~/sorted_photos --copy
```

## ⚠️ 5. 注意事项

### 环境管理
‼️ 强烈建议使用Conda环境运行，避免包依赖冲突

### 文件冲突
- 当禁用重命名时：
  - 目标目录存在同名文件会报错
  - 建议搭配`--copy`参数进行首次整理

### 扩展名处理
- 保留原始文件扩展名，并自动转换为小写格式（例：`.JPG` → `.jpg`）

### 误差计算逻辑
- 宽高比误差 = max(宽,高) / min(宽,高) ≤ 1.05

## 📚 6. 目录结构
输出目录自动生成结构：
```
image-classification/
├─ test/    # 测试文件夹
├─——— images/   # 测试用图片
├─ main.py  # 主程序
└─ requirements.txt # 依赖清单
```

## 📄 7. 许可协议
[Apache License](/LICENSE)