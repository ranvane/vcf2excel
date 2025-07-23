# VCF 转 Excel 工具

一个基于 Python 和 PySide6 的小工具，支持将通讯录 VCF 文件转换为 Excel 表格，支持多号码多列显示，并可搜索联系人。

---

## 功能特点

- 解析 VCF 文件，自动去除照片等大字段，避免解析错误  
- 支持联系人多个电话号码，多列显示  
- 联系人姓名排序，支持简单搜索过滤  
- 可自定义选择 VCF 文件和保存 Excel 文件路径  
- 友好的图形用户界面，使用 PySide6 实现  

---

## 环境依赖

- Python 3.8 及以上  
- vobject  
- xlsxwriter  
- PySide6  

安装依赖：

```bash
pip install vobject xlsxwriter PySide6
```

---

## 使用说明

1. 运行程序：

```bash
python vcf_to_excel_gui.py
```

2. 点击 **选择VCF文件** 按钮，选择你的 .vcf 通讯录文件  
3. 在联系人列表中可以搜索姓名  
4. 点击 **另存为Excel文件** 按钮，选择保存的 Excel 文件路径（*.xlsx）  
5. 程序会自动将联系人导出到 Excel 文件，并弹出提示

---

## 注意事项

- VCF 文件请确保编码为 UTF-8，且格式符合标准  
- 大型 VCF 文件解析时间可能稍长，请耐心等待  
- 程序会自动忽略含有照片字段的内容，避免解析失败  

---
## 打包命令
```
python -m nuitka --onefile --enable-plugin=pyside6 --windows-disable-console --output-dir=dist --jobs=auto  vcf_to_excel_gui.py


```

---

## 许可协议

MIT License


