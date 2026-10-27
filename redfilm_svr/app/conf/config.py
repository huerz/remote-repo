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
# 电影海报目录：独立成一个文件夹，按电影类型分子目录存放，方便直接打开替换
#   电影海报/动作片/、电影海报/科幻片/、电影海报/剧情片/ ...
#   接口仍按“文件名”访问，蓝图里会自动在子目录中查找
IMAGE_CLS_PATH = r'D:/高级网页设计/电影海报'
# 用户头像、站点 Logo 等图片的路径（与红影赏析共用同一套）
IMAGE_HEAD_PATH = r'D:/高级网页设计/images/head'

# 上传文件时，允许的文件扩展名的集合（教材 8.2.2）
ALLOWED_EXTENSIONS = set(['png', 'gif', 'jpg', 'webp', 'jpeg'])
