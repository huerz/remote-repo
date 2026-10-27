from flask import Blueprint, jsonify, send_from_directory
from werkzeug.exceptions import NotFound
import os
# 导入图片路径
from app.conf.config import IMAGE_CLS_PATH, IMAGE_HEAD_PATH

# ============================================================================
# 本文件接口清单（蓝图前缀 /api/image，在 app/__init__.py 注册时指定）
# ----------------------------------------------------------------------------
#   GET /api/image/display/<type>/<filename>   返回图片二进制流
#       路径参数 type     ：cls（电影海报图集，按电影类型分子目录）
#                           或 head（头像/Logo 图集）
#       路径参数 filename ：图片文件名，如 logo.png、jys.jpg
#                           也支持带类型子目录，如 唐诗/jys.jpg
#       物理路径映射      ：cls  → IMAGE_CLS_PATH = images/films/<电影类型>/
#                           head → IMAGE_HEAD_PATH = images/head/
#       查找规则          ：先按原样拼路径；找不到再按“文件名”递归查子目录，
#                           所以数据库里 cover 只存文件名即可，无需改数据
#       返回             ：图片流（Content-Type 由扩展名自动判定）
#                          文件不存在 → 404 {code:'404', msg:'图片不存在！'}
# ----------------------------------------------------------------------------
# 目录规范（共享图集库，各项目共用）：
#   D:/高级网页设计/images/
#     ├── films/动作片|科幻片|剧情片|动画片|喜剧片|悬疑片/
#     └── head/    logo.png、tx.png 等
# ----------------------------------------------------------------------------
# 前端调用示例（加代理前缀 /svr）：
#   /svr/api/image/display/head/logo.png
#   /svr/api/image/display/cls/jys.jpg
#   /svr/api/image/display/cls/唐诗/jys.jpg
# ============================================================================

# 创建蓝图
image_blueprint = Blueprint("image_blueprint", __name__)

# 文件名 -> 相对 IMAGE_CLS_PATH 的路径，例如 'jys.jpg' -> '唐诗/jys.jpg'
# 首次访问时建立，文件名没命中时重建一次（新增图片无需重启服务）
_cls_index = {}


def _build_cls_index():
    """递归扫描封面图集目录，建立“文件名 -> 相对路径”的索引。"""
    index = {}
    if os.path.isdir(IMAGE_CLS_PATH):
        for root, _dirs, files in os.walk(IMAGE_CLS_PATH):
            for name in files:
                rel = os.path.relpath(os.path.join(root, name), IMAGE_CLS_PATH)
                # 统一用正斜杠：Werkzeug 的 safe_join 不认 Windows 反斜杠，
                # 反斜杠路径会被判定为非法而抛 404
                index.setdefault(name, rel.replace(os.sep, '/'))
    return index


def _resolve_cls(filename):
    """把请求的文件名解析成相对 IMAGE_CLS_PATH 的路径，找不到返回 None。"""
    global _cls_index
    # 1) 允许直接传相对路径，如 display/cls/唐诗/jys.jpg
    if os.path.isfile(os.path.join(IMAGE_CLS_PATH, filename)):
        return filename.replace(os.sep, '/')
    # 2) 只传文件名时，在类型子目录中查找
    if not _cls_index:
        _cls_index = _build_cls_index()
    rel = _cls_index.get(os.path.basename(filename))
    if rel is None:
        # 可能是刚归档进来的新图，重建一次索引再找
        _cls_index = _build_cls_index()
        rel = _cls_index.get(os.path.basename(filename))
    return rel


# ============================================================================
# 【接口】图片显示
# 调用方式：GET /api/image/display/<string:type>/<path:filename>
# 参数：type（cls/head）、filename（图片文件名或“类型/文件名”）
# 返回：图片二进制流；不存在时 404 + JSON
# ============================================================================
@image_blueprint.route('/display/<string:type>/<path:filename>')
def display(type, filename):
    # 参数校验
    if not type or not filename:
        return jsonify({"code": "404", "msg": "参数错误！"}), 404

    # 电影海报：在按电影类型划分的子目录中查找
    # type 同时接受 film（新命名）与 cls（古典文学网沿用的旧命名），避免旧页面 404
    if type in ("film", "cls"):
        rel_path = _resolve_cls(filename)
        if rel_path is None:
            return jsonify({"code": "404", "msg": "图片不存在！"}), 404
        try:
            return send_from_directory(IMAGE_CLS_PATH, rel_path)
        except NotFound:
            return jsonify({"code": "404", "msg": "图片不存在！"}), 404

    # 头像 / Logo
    if os.path.isfile(os.path.join(IMAGE_HEAD_PATH, filename)):
        try:
            return send_from_directory(IMAGE_HEAD_PATH, filename)
        except NotFound:
            return jsonify({"code": "404", "msg": "图片不存在！"}), 404
    return jsonify({"code": "404", "msg": "图片不存在！"}), 404
