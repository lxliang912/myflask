# 认证蓝图模块
import functools
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)

from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

# 创建一个名为auth的蓝图
bp = Blueprint('auth', __name__, url_prefix='/auth')


# 关联register视图函数
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # 映射提交的键和值
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'username is required'
        elif not password:
            error = 'password is required'
        # 查询数据库username是否已存在,fetchone根据查询返回一个记录行
        elif db.execute('SELECT id FROM user WHERE username = ?',
                        (username, )).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            # 验证成功,在数据库中插入数据
            db.execute('INSERT INTO user (username, password) VALUES (?, ?)',
                       (username, generate_password_hash(password)))
            db.commit()
            return redirect((url_for('auth.login')))
        #  用于储存在渲染模块时可以调用的信息
        flash(error)

    return render_template('auth/register.html')


# 登录视图
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        # 查询用户是否在数据库中
        user = db.execute('SELECT * FROM user WHERE username = ?',
                          (username, )).fetchone()

        # 判断用户名是否正确
        print(user)
        if user is None:
            error = 'incorrect username'
        # 判断密码是否正确,比较哈希值
        elif not check_password_hash(user['password'], password):
            error = 'incorrect password'
            print(password)

        if error is None:
            # session用于储存横跨请求的值, 请求成功则id存于新会话中
            session.clear()
            session['user_id'] = user['id']
            return redirect((url_for('index')))

        flash(error)

    return render_template('auth/login.html')


# 注册一个 在视图函数之前运行的函数
@bp.before_app_request
# 检查用户 id 是否已经储存在 session 中，并从数据库中获取用户数据，然后储存在 g.user 中
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?',
                                  (user_id, )).fetchone()


# 注销的时候需要把用户 id 从 session 中移除
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# 在其他视图中验证
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view