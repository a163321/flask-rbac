from datetime import timedelta


def get_db_uri(dbinfo):
    engine = dbinfo.get("ENGINE")
    driver = dbinfo.get("DRIVER")
    user = dbinfo.get("USER")
    password = dbinfo.get("PASSWORD")
    host = dbinfo.get("HOST")
    port = dbinfo.get("PORT")
    name = dbinfo.get("NAME")

    return "{}+{}://{}:{}@{}:{}/{}".format(engine, driver, user, password, host, port, name)


class Config:
    DEBUG = False

    TESTING = False

    SECRET_KEY = "wertyuiodfghjkl!@#$%^&I(*&^5"

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    PERMANENT_SESSION_LIFETIME = timedelta(seconds=3600)  # 设置session有效时间为1个小时


class DevelopConfig(Config):
    DEBUG = True

    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "flask_demo",
        "PASSWORD": "BRJe4wbErBB4WdRK",
        "HOST": "114.215.102.141",
        "PORT": "3306",
        "NAME": "flask_demo"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class TestingConfig(Config):
    TESTING = True


class StagingConfig(Config):
    pass


class ProductConfig(Config):
    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "flask_demo",
        "PASSWORD": "BRJe4wbErBB4WdRK",
        "HOST": "114.215.102.141",
        "PORT": "3306",
        "NAME": "flask_demo"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)

    pass


envs = {
    "develop": DevelopConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "product": ProductConfig,
    "default": DevelopConfig,
}
