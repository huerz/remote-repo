from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy

from typing import Optional
from sqlalchemy import Integer
from sqlalchemy.dialects.mysql import  VARCHAR
from sqlalchemy.orm import Mapped, mapped_column
from flask_marshmallow import Marshmallow

# ============================================================================
# 本文件接口清单（单文件 Flask 练习项目，无蓝图前缀）
# ----------------------------------------------------------------------------
#   GET /add      新增 3 条用户数据（xiaoming / xiaoli / xiaozhu）
#   GET /search   查询全部用户（Marshmallow 序列化为 JSON）
#   GET /update   把 uid=2 的用户昵称改为「李白」
#   GET /delete   删除 uid=3 的用户（不存在时返回 code 404）
# ----------------------------------------------------------------------------
# 启动：.venv\Scripts\python.exe app.py
# 访问：http://127.0.0.1:5663/add  （每个接口都是 GET，浏览器可直接打开）
# 数据库：mysql+pymysql://root@127.0.0.1:3306/classicsdb 表 users
# ============================================================================

app = Flask(__name__)
# 载入数据库配置
# MySql连接的URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/classicsdb?charset=utf8' 
#  记录所有发送到标准输出的SQL语句，通常在开发调试时很有帮助。

#显示中文
app.json.ensure_ascii = False

app.config['SQLALCHEMY_ECHO'] = True 
# 创建数据库的操作对象
db = SQLAlchemy(app)
# 初始化 Marshmallow
ma = Marshmallow(app)

# ============================================================================
# 【接口 1】新增用户数据
# 调用方式：GET /add
# 参数：无（数据写死在函数内）
# 返回：{code:200, msg:'操作成功'}
# ============================================================================
# 1.增加用户数据
@app.route('/add')
def add_user():
       
    # 新建用户对象
    user1 = Users(uname='xiaoming',upwd='123456',nickname='小明',avatar='xm.jpg',sex='男',phone='13605689563')
    user2 = Users(uname='xiaoli',upwd='123456',nickname='小李',avatar='xl.jpg',sex='男',phone='15632365895')
    user3 = Users(uname='xiaozhu',upwd='123456',nickname='小朱',avatar='xz.jpg',sex='女',phone='18965324568')
    # 创建用户列表
    users = [user2,user3]
    # 使用 add() 将用户实例添加到数据库会话中 
    db.session.add(user1)
    # 使用 add_all() 将所有用户实例添加到数据库会话中 
    db.session.add_all(users)
    # 提交数据库
    db.session.commit()   
        
    return jsonify({"code":200,"msg":"操作成功"})

# ============================================================================
# 【接口 2】查询全部用户
# 调用方式：GET /search
# 参数：无
# 返回：[{uid, uname, upwd, nickname, avatar, sex, phone, remark}, ...]
# ============================================================================
# 2.查询用户数据
@app.route('/search')
def seach_user():
       
    # # 简单查询
    # users = Users.query.all()  # 查询所有用户数据
    # count = Users.query.count()  # 查询有多少个用户
    # user = Users.query.first()  # 查询第1个用户

    # # 根据uid查询  返回模型对象/None
    # user = Users.query.get(5)
    # users = Users.query.filter_by(uid=5).all()
    # user = Users.query.filter(Users.uid == 5).first()

    # # 查询昵称以某个字符开始/结尾/包含的所有用户
    # users = Users.query.filter(Users.nickname.endswith("g")).all()
    # users = Users.query.filter(Users.nickname.startswith("w")).all()
    # users = Users.query.filter(Users.nickname.contains("n")).all()
    # users = Users.query.filter(Users.nickname.like("%白%")).all()  # 模糊查询

    # # 查询账号不等于xiaomi的所有用户
    # from sqlalchemy import not_, and_, or_
    # users = Users.query.filter(not_(Users.uname == "xiaomi")).all()
    # users = Users.query.filter(Users.uname != "xiaomi").all()
    
    # # 查询uid在某个范围的用户
    # users = Users.query.filter(Users.uid.in_([1, 5, 6])).all()  
    # # 排序查询:所有用户按uid从大到小排序, 取前5个    
    # Users.query.order_by(Users.uid.desc()).limit(5).all()  
    
    # # 分页查询:每页3个，查询第2页的数据
    # # page: 哪一个页
    # # per_page: 每页多少条数据
    # # Error_out: False 查不到不报错
    # page = 2
    # per_page = 3
    # paginate = Users.query.paginate(page=page, per_page=per_page, error_out=False)
    
    # # paginate .pages: 共有多少页
    # # paginate .items: 当前页数的所有对象
    # # paginate .page: 当前页
   
	# # 去重昵称重复的用户记录
    # users = Users.query.distinct(Users.nickname).all()

    users = Users.query.all()
    # 创建usersSchema转换类，其中many=True为转换多条数据
    usersSchema = UsersSchema(many=True)
    # 将用户类别转换为JSON数据列表
    users_json = usersSchema.dump(users)
        
    return jsonify(users_json)
# ============================================================================
# 【接口 3】更新用户数据
# 调用方式：GET /update
# 参数：无（固定把 uid=2 的昵称改为「李白」）
# 返回：{code:200, msg:'操作成功'}
# ============================================================================
# 3.更新用户数据
@app.route('/update')
def update_user():
       
    # 返回主键为2的对应用户
    user = Users.query.get(2)
    # 修改用户昵称
    user.nickname = '李白'    
    # 提交会话以保存更改  
    db.session.commit()   
        
    return jsonify({"code":200,"msg":"操作成功"})
# ============================================================================
# 【接口 4】删除用户数据
# 调用方式：GET /delete
# 参数：无（固定删除 uid=3）
# 返回：{code:200, msg:'操作成功'} / {code:404, msg:'用户不存在：uid=3'}
# ============================================================================
# 4.删除用户数据
@app.route('/delete')
def delete_user():
       
    # 返回主键为3的对应用户
    user = Users.query.get(3)
    # 本机库里的 uid 是 1/2/3，取不到时返回 404，避免 db.session.delete(None) 抛 500
    if user is None:
        return jsonify({"code": 404, "msg": "用户不存在：uid=3"})
    # 删除用户数据
    db.session.delete(user)
    # 提交会话以保存更改  
    db.session.commit()   
        
    return jsonify({"code":200,"msg":"操作成功"})

# Users模型类，关联users数据库表
class Users(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'comment': '用户表'}

    uid: Mapped[int] = mapped_column(Integer, primary_key=True, comment='用户编号')
    uname: Mapped[str] = mapped_column(VARCHAR(100), comment='登录账号')
    upwd: Mapped[str] = mapped_column(VARCHAR(100), comment='登录密码')
    nickname: Mapped[Optional[str]] = mapped_column(VARCHAR(100), comment='昵称')
    avatar: Mapped[Optional[str]] = mapped_column(VARCHAR(200), comment='头像')
    sex: Mapped[Optional[str]] = mapped_column(VARCHAR(50), comment='性别')
    phone: Mapped[Optional[str]] = mapped_column(VARCHAR(50), comment='电话')
    remark: Mapped[Optional[str]] = mapped_column(VARCHAR(200), comment='备注')
    
# 使用 flask-marshmallow 自动生成schema  
class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users 
        # 序列化的字段
        fields = ("uid", "uname", "upwd", "nickname", "avatar", "sex", "phone", "remark")

if __name__ == "__main__":
    # 首次运行时按模型自动建表（表已存在则跳过，可反复执行，不影响已有数据）
    # 没有这一步：库存在但表不存在 -> 所有访问数据库的路由都会 500
    with app.app_context():
        db.create_all()
    app.run(port=5663)