# ============================================================================
# mod_wsgi 入口（教材 9.3.3 部署方式）
# ----------------------------------------------------------------------------
# 作用：给 Apache 的 mod_wsgi 提供 WSGI 可调用对象，让 Apache 直接加载 Flask 应用，
#       不需要另开 Python 进程（与本目录 run_prod.py 的 waitress 方案二选一）。
# 用法：在 httpd.conf 中配置
#       WSGIScriptAlias /api "D:/高级网页设计/cls_svr/wsgi.py"
#       并给该文件所在目录 Require all granted
# 依赖：mod_wsgi 模块（编译安装见 部署说明.md 第 3 节）
# 约定：文件名必须叫 wsgi.py 且导出名为 application 的变量，mod_wsgi 只认这个名字。
# ============================================================================
from __future__ import annotations

import os
import sys

# mod_wsgi 启动时的工作目录不一定是项目根，显式把 cls_svr 加进模块搜索路径，
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 否则 import app 会失败。
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app  # noqa: E402  （必须在 sys.path 调整之后导入）

application = create_app()  # mod_wsgi 约定的入口变量名，不要改名
