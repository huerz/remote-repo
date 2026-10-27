# -------- 数据库配置 --------
# 教材配置（项目 9 部署时也用这个）：MySQL 8.4
MYSQL_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/redfilmdbs?charset=utf8'

# 离线兜底：MySQL 没启动时自动改用同目录的 SQLite 文件
#   目的：没装 / 没起 MySQL 也能把页面跑出内容，方便演示与验收
#   一旦 MySQL 起来，下次启动会自动切回 MySQL，无需改代码
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SQLITE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'redfilmdbs.db')


def _mysql_ready():
    """探测本机 MySQL 是否可用：既要连得上，也要目标库已存在。

    只测「连得上」不够——MySQL 起着但库没建时，SQLAlchemy 会在第一次查询时
    抛 1049 Unknown database，比直接走 SQLite 兜底更难排查。
    """
    try:
        import pymysql
        conn = pymysql.connect(
            host='127.0.0.1', port=3306, user='root',
            password='123456', connect_timeout=1
        )
        try:
            with conn.cursor() as cur:
                cur.execute("SHOW DATABASES LIKE 'redfilmdbs'")
                exists = cur.fetchone() is not None
        finally:
            conn.close()
        return exists
    except Exception:
        return False


# 有 MySQL 用 MySQL，没有就用 SQLite
SQLALCHEMY_DATABASE_URI = MYSQL_URI if _mysql_ready() else SQLITE_URI

# 记录所有发送到标准输出的 SQL 语句，这通常在开发调试时很有用
# 走 SQLite 兜底时关掉，避免刷屏
SQLALCHEMY_ECHO = SQLALCHEMY_DATABASE_URI == MYSQL_URI
