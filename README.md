# workform
工单系统

任务工单系统

    安装：
        1) django install
            pip install django | easy_install django
        2) pillow
            pip install Pillow | easy_install Pillow
        3) 初始化
            python3 manage.py makemigrations
            python3 manage.py migrate

    运行：
        1) pycharm
            使用pycharm打开项目，添加app后，就可以直接运行了
        2) 命令行
            进到项目的根目录执行：  python3 manage.py runserver 127.0.0.1:8000

功能介绍：
    login:
        http://127.0.0.1:8000/login

    注册:
        http://127.0.0.1:8000/register

    任务提交:
        http://127.0.0.1:8000/new_project

    任务详细：
        http://127.0.0.1:8000/backlog.html

    api（需要提交post请求）:
        http://127.0.0.1:8000/api
        eg: http://127.0.0.1:8000/api?type_data=project_data
        api支持两种类型：
            1) project_data
            2) domain_info

    文件上传:
        http://127.0.0.1:8000/upload

    组合搜索:
        http://127.0.0.1:8000/article-0-0.html

    目录结构:
        static/            存放静态文件 css/js/jpg/....
        form_work          项目主站
        templates          存放 html文件
        utils              存放 插件文件 分布、验证码
        work               app
        work/views.py      视图函数，除登陆外的
        work/view          视图函数，有登陆、验证码、api功能
        work/models.py     数据库操作功能
        db.sqlite3         sqlite3 数据库文件
