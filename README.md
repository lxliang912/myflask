# myflask

基于flask框架开发的python后端模板


## 项目结构
### setup
* 创建工程所需的依赖

### app文件夹存放项目代码
#### py文件说明
* app.py 用于启动应用
* config.py 用于配置数据库、api名称的相关配置信息
* reference.py 初始化引用的扩展，如SQLAlchemy、Api
* router.py 配置路由接口

#### 文件夹说明
##### utils文件夹
* 存放封装的工具库及方法
##### 类模板（如task）
* 独立各个接口开发
* model.py 实现相关的数据库操作
* view.py 实现各接口请求相关操作

## 数据库
* 此项目使用的是mysql数据库，需自行安装，并在config.py中修改数据库名称为自己的

## 启动项目
1. 创建虚拟环境，执行命令：venv\Scripts\activate
2. 运行应用：
>在 Linux and Mac 下：
>* export FLASK_APP=app/app.py
>* export FLASK_ENV=development
>* flask run
>
>在 Windows 下，使用 set 代替 export ：
>* set FLASK_APP=app/app.py
>* set FLASK_ENV=development
>* flask run
>
>在 Windows PowerShell 下，使用 $env: 代替 export ：
>* $env:FLASK_APP = "app/app.py"
>* $env:FLASK_ENV = "development"
>* flask run