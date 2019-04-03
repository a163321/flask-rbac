from flask_wtf import FlaskForm  # FlaskForm 为表单基类
from wtforms import StringField, IntegerField, SelectField, PasswordField  # 导入字符串字段，密码字段，提交字段
from wtforms.validators import DataRequired, ValidationError
from app.models import ManageUser
from app.common import AdminException


class ManageForm(FlaskForm):
    id = IntegerField()

    username = StringField(
        validators=[
            DataRequired('请输入用户名')
        ],
    )

    password = StringField()
    password_confirm = StringField()
    status = IntegerField()

    def validate_password_confirm(self, field):
        id = self.id.data
        if not id:
            if not self.password.data:
                raise ValidationError('请输入登录密码')
            if self.password.data != self.password_confirm.data:
                raise ValidationError('两次密码输入不一致')
        else:
            if self.password.data:
                if self.password.data != self.password_confirm.data:
                    raise ValidationError('两次密码输入不一致')

    def validate_username(self, field):
        id = self.id.data
        modal = ManageUser()
        result = modal.check_name_exist(self.username.data, id)
        if result:
            raise ValidationError('此用户名已被使用了')

    def save(self, role_id):
        id = self.id.data
        username = self.username.data
        password = self.password.data
        status = self.status.data

        if len(role_id) <= 0:
            raise AdminException('请选择角色')

        modal = ManageUser()
        if not id:
            modal.save(username=username, password=password, role_id=role_id, status=status)
        else:
            modal.edit(username=username, password=password, role_id=role_id, id=id, status=status)
