# -------- MySQL 数据库配置 --------
# MySQL 连接的 URI
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/classicsdb?charset=utf8'
# 记录所有发送到标准输出的 SQL 语句，这通常在开发调试时很有用
SQLALCHEMY_ECHO = True

