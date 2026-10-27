# 项目常用配置
# ------ JSON编码配置 ------
ENSURE_ASCII = False  # 设置是否对JSON数据进行ascii编码

# 项目常用配置
# -------JWT 配置-------
JWT_SECRET_KEY = 'jwt_xiaobai_168'  # 设置 JWT 的密钥
# 设置访问令牌的过期时间，默认为 15min
JWT_ACCESS_TOKEN_EXPIRES = 15

# -------图片路径配置-------
# 共享图集库根目录（放在 D:/高级网页设计/images，各项目共用）
IMAGE_ROOT = r'D:/高级网页设计/images'
# 文学作品封面图片的路径：按文学类型分子目录存放
#   images/books/诗经/、images/books/楚辞/、images/books/唐诗/ ...
IMAGE_CLS_PATH = r'D:/高级网页设计/images/books'  # 接口仍按“文件名”访问，蓝图里会自动在子目录中查找
IMAGE_HEAD_PATH = r'D:/高级网页设计/images/head'  # 用户头像、站点 Logo 等图片的路径

ALLOWED_EXTENSIONS = set(['png', 'gif', 'jpg', 'webp', 'jpeg'])  # 上传文件时，允许的文件扩展名的集合（教材 8.2.2）