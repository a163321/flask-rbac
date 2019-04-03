from app.extension import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.ManageRole import ManageRole
from app.common import AdminException
import time

manager_user_role = db.Table(
    'manager_user_role',
    db.Column('manage_user_id', db.Integer, db.ForeignKey('manage_user.id'), primary_key=True),
    db.Column('manage_role_id', db.Integer, db.ForeignKey('manage_role.id'), primary_key=True)
)


class ManageUser(db.Model):
    __tablename__ = 'manage_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), index=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    status = db.Column(db.SmallInteger, nullable=False, default=1)
    is_super = db.Column(db.SmallInteger, nullable=True, default=0)
    create_time = db.Column(db.Integer, index=True, default=0)
    update_time = db.Column(db.Integer, index=True, default=0)

    roles = db.relationship('ManageRole', secondary=manager_user_role, backref=db.backref('manages', lazy='dynamic'),
                            lazy='dynamic')

    # 通过账号查询数据
    def get_user_by_account(self, account):
        user_info = self.query.filter_by(username=account).first()
        return user_info

    # 判断密码是否正确
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # 生成密码
    def make_password(self, password):
        return generate_password_hash(password)

    def check_name_exist(self, name, id=0):
        if id:
            filters = {
                ManageUser.username == name,
                ManageUser.id != id
            }
        else:
            filters = {
                ManageUser.username == name,
            }

        count = self.query.filter(*filters).count()
        return count

    def save(self, username, role_id, password, status):
        time_stamp = time.time()
        roles = ManageRole.query.filter(ManageRole.id.in_(role_id)).all()
        user = ManageUser(username=username,
                          password=self.make_password(password),
                          create_time=time_stamp,
                          update_time=time_stamp,
                          roles=roles,
                          status=status
                          )
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            raise AdminException('保存失败')

    def edit(self, username, role_id, id, status, password=''):
        user = self.query.filter_by(id=id).first()
        if not user:
            raise AdminException('用户不存在')

        user.username = username
        user.update_time = time.time()
        user.status = status

        if password:
            user.password = self.make_password(password)

        old_role = user.roles.all()
        for role_item in old_role:
            role_item.manages.remove(user)

        roles = ManageRole.query.filter(ManageRole.id.in_(role_id)).all()
        for role_item in roles:
            user.roles.append(role_item)

        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            raise AdminException('保存失败')

    def delete_user(self, user_id):
        user = self.query.filter_by(id=user_id).first()
        if not user:
            raise AdminException('用户不存在')

        old_role = user.roles.all()
        for role_item in old_role:
            role_item.manages.remove(user)

        try:
            db.session.delete(user)
            db.session.commit()
        except:
            db.session.rollback()
            raise AdminException('删除失败')

    def get_manage_access(self, user):
        roles = user.roles.all()
        access_paths = []
        for role in roles:
            access = role.access.all()
            for item in access:
                access_paths.append(item.path)

        return access_paths
