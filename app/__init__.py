from flask import Flask
from flask_moment import Moment

from app.extension import init_ext
from app.views import init_blue
from app.config import envs


def create_app(env):
    app = Flask(__name__)
    moment = Moment(app)

    # 初始化App的配置
    app.config.from_object(envs.get(env))

    # 初始化第三方的插件
    init_ext(app=app)

    # 加载中间件
    # load_middleware(app=app)

    # 初始化路由系统
    init_blue(App=app)
    return app
