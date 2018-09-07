import os
from flask import Flask
from . import db, auth, blog


def create_app(test_config=None):
    # 创建一个Flask实例
    app = Flask(__name__, instance_relative_config=True)
    # 设置一个应用的缺省配置
    app.config.from_mapping(
        # 用于保证数据安全，开发时设为dev，发布时用随机数重载
        SECRET_KEY='dev',
        # 数据库存放路径，位于Flask存放实例的app.instance_path内
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # 如果config.py文件存在，使用其中的值来重载缺省配置
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        # 确保app.instance_path的存在
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    # 导入并注册蓝图
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    app.add_url_rule('/', endpoint='index')

    return app
