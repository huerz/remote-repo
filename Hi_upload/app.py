# -*- coding: utf-8 -*-
"""
Hi_upload · 教材项目 8「古典文学网」用户中心模块 · 8.2.1 / 8.2.2 知识储备

本文件接口清单：
    1) POST /upload                          上传文件（form-data，参数名 file）
    2) GET  /download/<filename>             下载文件（send_file 实现）
    3) GET  /download-from-dir/<filename>    下载文件（send_from_directory 实现）

说明：
    - 教材 8.2.2 给了两种下载写法（send_file / send_from_directory），
      两段代码在教材里都写作 @app.route('/download/<filename>')。
      同一路由不能注册两次（Flask 会报端点冲突），所以这里把第二种
      改成 /download-from-dir/<filename>，两种都能单独测试。
    - 启动端口：教材用 5000；本机统一随机到 5000-5900 段，本示例用 5337。
"""
import os
import uuid

from flask import Flask, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename

# 导入上传的配置（路径、文件扩展名的集合）
from config import FILE_PATH, ALLOWED_EXTENSIONS

app = Flask(__name__)


def allowed_file(filename):
    """判断文件类型是否允许上传（教材 8.2.1）"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ------------------------------------------------------------------ 上传
@app.route('/upload', methods=["POST"])
def upload():
    """上传文件（教材 8.2.1 / 图 8.2）

    调用方式：POST /upload
    请求体：form-data，key = file
    返回：{"code":"200","msg":"上传成功！","upFile":"<uuid>.<ext>"}
    """
    # 返回信息
    result_msg = {"code": "200", "msg": "上传成功！"}

    # 判断是否存在上传文件（file 是上传文件的参数名称）
    if 'file' not in request.files:
        result_msg["code"] = "404"
        result_msg["msg"] = "文件不存在！"
        return jsonify(result_msg)

    # 判断存放目录是否存在，若不存在则创建对应目录
    if not os.path.exists(FILE_PATH):
        os.makedirs(FILE_PATH)

    # 获取上传文件
    upfile = request.files['file']

    # 判断文件是否允许上传
    if upfile and allowed_file(upfile.filename):
        # 获取文件名称
        upname = secure_filename(upfile.filename)
        # 为处理重名情况，使用 uuid 生成文件名
        # 注意：secure_filename() 会过滤掉中文等非 ASCII 字符，
        #       中文文件名可能只剩扩展名（甚至为空），这里补一层兜底，
        #       否则教材原写法会因 rsplit('.', 1)[1] 越界而 500。
        if '.' in upname:
            ext = upname.rsplit('.', 1)[1].lower()
        else:
            ext = upfile.filename.rsplit('.', 1)[-1].lower()
        fname = str(uuid.uuid4()) + '.' + ext
        # 保存文件到存放目录
        upfile.save(os.path.join(FILE_PATH, fname))
        result_msg["upFile"] = fname
    else:
        # 构建返回的 JSON 格式的数据
        result_msg["code"] = "400"
        result_msg["msg"] = "上传失败！"

    # 返回操作结果
    return jsonify(result_msg)


# ------------------------------------------------- 下载（方式一：send_file）
@app.route('/download/<filename>')
def download_file(filename):
    """下载文件（教材 8.2.2 第 1 种：send_file / 图 8.3）"""
    # 构建下载文件的路径
    file_path = os.path.join(FILE_PATH, filename)
    if not os.path.exists(file_path):
        return jsonify({"code": "404", "msg": "文件不存在！"}), 404
    # 使用 send_file() 函数发送文件
    # as_attachment=True 告诉浏览器这是附件，应下载而不是直接打开
    # download_name 指定下载时保存的文件名
    return send_file(file_path, as_attachment=True, download_name=filename)


# --------------------------------- 下载（方式二：send_from_directory）
@app.route('/download-from-dir/<filename>')
def download(filename):
    """下载文件（教材 8.2.2 第 2 种：send_from_directory / 图 8.4）

    与方式一的区别：
        send_file            需要自己拼完整路径；
        send_from_directory  只给「目录 + 文件名」，自带路径安全检查。
    """
    # 检查文件名是否安全（防止目录遍历等攻击）
    if '..' in filename or filename.startswith('/'):
        return "Bad Request", 400
    # as_attachment=True 告诉浏览器这是一个附件，应该下载它而不是直接打开它
    return send_from_directory(FILE_PATH, filename, as_attachment=True)


if __name__ == '__main__':
    # 启动服务，设置主机和端口
    # 教材：app.run(host='127.0.0.1', port=5000, debug=True)
    app.run(host='127.0.0.1', port=5337, debug=True)
