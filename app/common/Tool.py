import json
import time


# 解析错误信息
def get_error(errors):
    errors = list(errors.values())
    error = errors[0][0]

    return error


# admin json数据返回
def admin_json_response(message, url='', code=1):
    return json.dumps({
        "code": code,
        "msg": message,
        "url": url
    })


# 时间格式化
def format_time(time_stamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_stamp))
