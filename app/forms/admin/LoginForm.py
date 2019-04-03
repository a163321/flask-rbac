from flask_wtf import FlaskForm  # FlaskForm 为表单基类
from wtforms import StringField, PasswordField  # 导入字符串字段，密码字段，提交字段
from wtforms.validators import DataRequired, ValidationError
from app.models import ManageUser
from flask import session


class LoginForm(FlaskForm):
    account = StringField(
        # 验证器
        validators=[
            DataRequired('请输入用户名')
        ],
        description="账号"
    )

    password = PasswordField(
        # 验证器
        validators=[
            DataRequired('请输入密码')
        ],
        description="密码"
    )

    def validate_password(self, field):
        # 判断密码是否正确
        account = self.account.data
        password = self.password.data

        modal = ManageUser()
        print(account)
        user_info = modal.get_user_by_account(account=account)
        print(user_info)
        if not user_info:
            raise ValidationError('用户名或者密码错误')

        if not user_info.check_password(password):
            raise ValidationError('用户名或者密码错误')

        if not user_info.status:
            raise ValidationError('账号已被禁用')

        # 保存session
        session.permanent = True  # 设置session有效时间
        session['admin_id'] = user_info.id
        return True
