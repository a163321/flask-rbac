from flask_wtf import FlaskForm  # FlaskForm 为表单基类
from wtforms import StringField, IntegerField, Field  # 导入字符串字段，密码字段，提交字段
from wtforms.validators import DataRequired, ValidationError
from app.common import AdminException
from app.models import ManageRole


class RoleForm(FlaskForm):
    id = IntegerField()

    role_name = StringField(
        validators=[
            DataRequired('请输入角色名称')
        ],
    )

    def save(self, role_name, access, id=0):
        if len(access) <= 0:
            raise AdminException('请选择权限')

        model = ManageRole()

        if model.check_name_exist(name=role_name, id=id):
            raise AdminException('此角色已存在了')

        if id:
            model.edit(role_name, access, id)
        else:
            model.add(role_name, access)
