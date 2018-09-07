import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    # g 为特殊事件,用于存储多个函数用到的数据,
    # 可多次使用,在不同的请求中每次调用get_db创建一个新的连接
    if 'db' not in g:
        # sqlite3.connect建立一个数据库连接,指向配置中的DATABASE指定文件
        g.db = sqlite3.connect(
            # current_app指向处理请求的flask英语
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # sqlite3.Row告诉连接返回类似于字典的行,通过列名称操作数据
        g.db.row_factory = sqlite3.Row
    return g.db


# 通过检查g.db确定连接是否建立
def close_db(e=None):
    db = g.pop('db', None)
    # 已建立连接则关闭连接
    if db is not None:
        db.close()


def init_db():
    # 返回一个数据库连接
    db = get_db()
    # 打开文件,文件名相对于flaskr包
    with current_app.open_resource('./schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
# 定义一个 init-db 的命令,用于调用init_db函数,调用init_db
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    # 返回响应后进行清理
    app.teardown_appcontext(close_db)
    # 添加一个与flask一起工作的命令
    app.cli.add_command(init_db_command)
