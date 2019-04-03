from flask_wtf import FlaskForm  # FlaskForm 为表单基类
from wtforms import StringField, IntegerField  # 导入字符串字段，密码字段，提交字段
from wtforms.validators import DataRequired, ValidationError
from app.models import ManageAccess
from app.common import AdminException


class AccessForm(FlaskForm):
    id = IntegerField()
    parent_id = IntegerField()

    access_name = StringField(
        validators=[
            DataRequired('请输入权限名称')
        ],
    )

    path = StringField(
        validators=[
            DataRequired('请输入权限url')
        ],
    )

    def validate_access_name(self, field):
        id = self.id.data
        name = self.access_name.data

        modal = ManageAccess()
        result = modal.check_name_exist(name, id)
        if result:
            raise ValidationError('此权限名称已存在了')

        return True

    def save(self):
        data = self.data
        del data["csrf_token"]
        try:
            modal = ManageAccess()
            modal.add_or_edit(**data)

        except AdminException as e:
            raise AdminException(e.message)
