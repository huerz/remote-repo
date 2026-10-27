# -*- coding: utf-8 -*-
"""
Hi_upload 配置文件（教材 8.2.1）

教材原文：
    FILE_PATH = r'D:\\upload_file'
    ALLOWED_EXTENSIONS = set(['png', 'gif', 'jpg', 'jpeg', 'jpe'])

本机调整：
    上传目录放到项目内的 upload_file 目录，不在 D:\\ 根目录新建目录
    （按用户要求：生成物 / 临时目录不落盘符根目录）。
    若想让行为与教材完全一致，把 FILE_PATH 改成 r'D:\\upload_file' 即可。
"""
import os

# 项目根目录（config.py 所在目录）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 文件上传后的存放目录（教材为 D:\upload_file，这里改到项目内）
FILE_PATH = os.path.join(BASE_DIR, 'upload_file')

# 允许上传的文件扩展名的集合（教材原文）
ALLOWED_EXTENSIONS = set(['png', 'gif', 'jpg', 'jpeg', 'jpe'])
