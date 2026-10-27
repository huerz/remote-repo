# -*- coding: utf-8 -*-
"""
hi_flash · 教材 7.2.2 Flask 框架的消息闪现

本文件接口清单：
    GET  /        首页（用 get_flashed_messages() 显示闪现消息）
    GET  /login   登录页
    POST /login   模拟登录（内置账号 admin / 密码 123456），
                  成功后 flash('您已成功登录！') 并 redirect 到首页

启动端口：教材用 5000；本机统一随机到 5000-5900 段，本示例用 5741。
"""
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = 'random string'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 错误提示
    error = None
    # 判断请求方式，此处 POST 请求方式对应登录操作
    if request.method == 'POST':
        # 获取账号及密码
        uname = request.form['uname']
        upwd = request.form['upwd']
        # 模拟登录操作，内置账号为 admin，密码为 123456
        if uname != 'admin' and upwd != '123456':
            error = '用户名或密码有误，请重新登录！'
        else:
            # 利用消息闪现机制传递消息到首页
            flash('您已成功登录！')
            # 跳转至首页
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


if __name__ == '__main__':
    # 启动服务，设置主机和端口
    app.run(host="0.0.0.0", port=5741, debug=True)
