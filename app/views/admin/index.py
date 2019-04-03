from flask import Blueprint, render_template, request, url_for, session, redirect
from app.forms.admin import LoginForm
import json

blue_admin_index = Blueprint("blue_admin_index",
                             __name__,
                             url_prefix='/admin',
                             template_folder='../../../templates',
                             static_folder='../../../static'
                             )


@blue_admin_index.route('/')
def index():
    return render_template('admin/index.html')


# 登录
@blue_admin_index.route('/login', methods=['GET', 'POST'])
def login():
    forms = LoginForm()
    if request.method == 'POST':
        validate = forms.validate()
        # print(validate)
        if not validate:
            errors = list(forms.errors.values())
            error = errors[0][0]

            return json.dumps({"code": 0, "msg": error})
        else:
            url = url_for('blue_admin_index.index')
            return json.dumps({"code": 1, "msg": '登录成功', "url": url})

    return render_template('admin/login.html', form=forms)


# 退出登录
@blue_admin_index.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blue_admin_index.login'))
