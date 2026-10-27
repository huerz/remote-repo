# ============================================================================
# 生产环境 WSGI 入口（waitress）
# ----------------------------------------------------------------------------
# 作用：用 waitress 在 5382 端口跑 Flask 应用，供 Apache 反向代理调用。
#       开发时用 run.py（Flask 自带服务器 + 热重载），线上用本文件。
# 用法：.venv\Scripts\python.exe run_prod.py
# 依赖：waitress（已加入 cls_svr/requirements.txt）
# 约定：只绑 127.0.0.1，外网访问一律经 Apache:8088，不直接暴露应用端口。
# ============================================================================
from __future__ import annotations

import sys

from waitress import serve

from app import create_app

HOST = '127.0.0.1'  # 监听地址与端口：与 vite 代理、Apache 转发配置保持一致
PORT = 5382

THREADS = 8  # 工作线程数：课程演示规模下 8 个足够，可按并发量调整


def main() -> int:
    """启动 waitress 服务。

    Returns:
        进程退出码，正常情况不会返回（serve 会一直阻塞）。
    """
    app = create_app()
    print(f'[生产模式] waitress 启动：http://{HOST}:{PORT}  线程 {THREADS}')
    serve(app, host=HOST, port=PORT, threads=THREADS)
    return 0


if __name__ == '__main__':
    sys.exit(main())
