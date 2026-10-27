# ============================================================================
# 切换到 mod_wsgi 部署方式（教材 9.3.2 / 9.3.3）
# ----------------------------------------------------------------------------
# 作用：把 httpd.conf 里「mod_proxy 反代 waitress」的配置换成「mod_wsgi 直连 Flask」，
#       切换后 Apache 自己加载 Python 应用，不需要再跑 run_prod.py。
# 用法：
#   启用：.venv\Scripts\python.exe switch_to_mod_wsgi.py
#   回滚：.venv\Scripts\python.exe switch_to_mod_wsgi.py --revert
# 依赖：调用前必须先执行
#       .venv\Scripts\mod_wsgi-express.exe module-config
#       （脚本会去 %TEMP%\mod_wsgi_config.txt 读这三行，或自己调用一次）
# 约定：改配置前自动备份为 httpd.conf.bak-mod_wsgi；改完必须重启 Apache 服务
# ============================================================================
from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys

# ---------------- 路径常量 ----------------
APACHE_HOME = pathlib.Path(r'D:/System/Apache24')
HTTPD_CONF = APACHE_HOME / 'conf' / 'httpd.conf'
BACKUP = APACHE_HOME / 'conf' / 'httpd.conf.bak-mod_wsgi'

PROJECT = pathlib.Path(r'D:/高级网页设计/cls_svr')
WSGI_SCRIPT = PROJECT / 'wsgi.py'
VENV_PY = PROJECT / '.venv' / 'Scripts' / 'python.exe'
MOD_WSGI_EXPRESS = PROJECT / '.venv' / 'Scripts' / 'mod_wsgi-express.exe'

PROXY_MARK = '# 反向代理：把 /svr/api 映射到 Flask 应用（端口 5382）'  # 代理模式的起始标记（切到 mod_wsgi 时整段注释掉）

WSGI_BLOCK = '''  # mod_wsgi 需要追加的配置块
# ============================================================================
# mod_wsgi 直连配置（教材 9.3.3）
# ----------------------------------------------------------------------------
# 与上面的 mod_proxy 方案二选一：启用本段后不用再跑 run_prod.py（waitress）
# ============================================================================
WSGIScriptAlias /api "{wsgi}"
<Directory "{proj}">
    <Files wsgi.py>
        Require all granted
    </Files>
</Directory>
WSGIApplicationGroup %{{GLOBAL}}  # C 扩展（PyMySQL 等）在多解释器下容易出问题，强制用主解释器

# 前端仍请求 /svr/api/...，这里把 /svr 前缀去掉，交给上面的 WSGIScriptAlias
LoadModule rewrite_module modules/mod_rewrite.so
RewriteEngine On
RewriteRule ^/svr(/.*)$ $1 [PT]
'''


def run_module_config() -> str:
    """调用 mod_wsgi-express module-config，拿到三行模块配置。

    Returns:
        形如 LoadFile / LoadModule / WSGIPythonHome 的配置文本。

    Raises:
        FileNotFoundError: mod_wsgi 还没装好（mod_wsgi-express 不存在）。
        RuntimeError: 命令执行失败。
    """
    if not MOD_WSGI_EXPRESS.exists():
        raise FileNotFoundError(
            '找不到 mod_wsgi-express，说明 mod_wsgi 还没装好。\n'
            '请先在管理员窗口执行 启用mod_wsgi.bat（会顺带装 VS 生成工具）。'
        )
    result = subprocess.run(
        [str(MOD_WSGI_EXPRESS), 'module-config'],
        capture_output=True, text=True, encoding='utf-8', errors='ignore'
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError(f'module-config 执行失败：{result.stderr.strip()}')
    return result.stdout.strip()


def apply(config_text: str) -> None:
    """把 httpd.conf 从代理模式改成 mod_wsgi 模式。

    Args:
        config_text: mod_wsgi-express module-config 输出的三行配置。
    """
    text = HTTPD_CONF.read_text(encoding='utf-8')
    if 'WSGIScriptAlias /api' in text:
        print('[跳过] httpd.conf 里已经有 WSGIScriptAlias，无需重复写入')
        return

    BACKUP.write_text(text, encoding='utf-8')
    print(f'[备份] {BACKUP}')

    # 1) 整段注释掉 ProxyPass 那几行，避免和 WSGIScriptAlias 抢 /api
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip().startswith(PROXY_MARK):
            for i in range(index, min(index + 6, len(lines))):
                if lines[i].strip() and not lines[i].lstrip().startswith('#'):
                    lines[i] = '# ' + lines[i]
                elif not lines[i].strip():
                    break
            print('[代理] 已注释掉 ProxyPass 配置段')
            break

    block = WSGI_BLOCK.format(wsgi=WSGI_SCRIPT.as_posix(), proj=PROJECT.as_posix())  # 2) 追加模块加载行 + WSGI 配置块
    new_text = '\n'.join(lines) + '\n\n' + config_text + '\n' + block
    HTTPD_CONF.write_text(new_text, encoding='utf-8')
    print('[写入] mod_wsgi 配置已追加到 httpd.conf')


def revert() -> None:
    """从备份恢复成代理模式。"""
    if not BACKUP.exists():
        print('[错误] 没有找到备份文件 httpd.conf.bak-mod_wsgi，无法回滚')
        sys.exit(1)
    shutil.copyfile(BACKUP, HTTPD_CONF)
    print('[回滚] 已用备份恢复 httpd.conf（ProxyPass 模式）')


def check_syntax() -> bool:
    """跑一次 httpd -t 做语法检查。"""
    result = subprocess.run(
        [str(APACHE_HOME / 'bin' / 'httpd.exe'), '-t'],
        capture_output=True, text=True, encoding='utf-8', errors='ignore'
    )
    output = (result.stdout + result.stderr).strip()
    print('[检查]', output)
    return 'Syntax OK' in output


def main(argv: list[str] | None = None) -> int:
    """入口：切换或回滚 mod_wsgi 配置。

    Args:
        argv: 命令行参数，支持 --revert。

    Returns:
        进程退出码：0 成功，1 失败（配置有错时不要重启服务）。
    """
    parser = argparse.ArgumentParser(description='切换 Apache 到 mod_wsgi 部署方式')
    parser.add_argument('--revert', action='store_true', help='回滚成 ProxyPass 模式')
    args = parser.parse_args(argv)

    if args.revert:
        revert()
        check_syntax()
        return 0

    try:
        config_text = run_module_config()
    except (FileNotFoundError, RuntimeError) as exc:
        print(f'[错误] {exc}')
        return 1

    print('[模块] 获取到配置：')
    for line in config_text.splitlines():
        print('   ', line)

    apply(config_text)
    if not check_syntax():
        print('[失败] httpd.conf 语法有问题，已保留备份，可用 --revert 回滚')
        return 1

    print('\n[下一步] 重启 Apache 让配置生效（管理员）：')
    print('    httpd.exe -k restart -n "apache2.4"')
    print('   或双击 启动站点.bat')
    return 0


if __name__ == '__main__':
    sys.exit(main())
