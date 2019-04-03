from app.extension import db
from app.models.ManageAccess import ManageAccess
from app.common import AdminException
import time

manager_role_access = db.Table(
    'manager_role_access',
    db.Column('manage_access_id', db.Integer, db.ForeignKey('manage_access.id'), primary_key=True),
    db.Column('manage_role_id', db.Integer, db.ForeignKey('manage_role.id'), primary_key=True)
)


class ManageRole(db.Model):
    __tablename__ = 'manage_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(40), index=True, nullable=False)
    create_time = db.Column(db.Integer, index=True, default=0)
    update_time = db.Column(db.Integer, index=True, default=0)

    access = db.relationship('ManageAccess', secondary=manager_role_access, backref=db.backref('roles', lazy='dynamic'),
                             lazy='dynamic')

    def get_all_access(self, role_id=0):
        role_access_ids = []
        if role_id:
            role = self.query.get(role_id)
            access = role.access.all()
            print(access)
            for access_item in access:
                role_access_ids.append(access_item.id)

        access_modal = ManageAccess()
        all_access = access_modal.get_all_access()

        return self.get_js_tree(role_access_ids, all_access)

    def get_js_tree(self, role_access_ids, all_access):
        js_tree = []
        for item in all_access:
            js_tree.append({
                "id": item.id,
                "parent": item.parent_id if item.parent_id > 0 else '#',
                "text": item.access_name,
                "state": {
                    "selected": 1 if item.id in role_access_ids and self.has_children(item.id, all_access,
                                                                                      role_access_ids) else 0
                }
            })

        return js_tree

    def has_children(self, access_id, all_access, role_access_ids):
        children_ids = []
        for item in all_access:
            if item.parent_id == access_id:
                children_ids.append(item.id)

        for item in children_ids:
            if item not in role_access_ids:
                return False

        return True

    def check_name_exist(self, name, id=0):
        if id:
            filters = {
                ManageRole.role_name == name,
                ManageRole.id != id
            }
        else:
            filters = {
                ManageRole.role_name == name,
            }

        count = self.query.filter(*filters).count()
        return count

    def add(self, role_name, access):
        time_stamp = time.time()

        access_list = ManageAccess.query.filter(ManageAccess.id.in_(access)).all()
        role = ManageRole(
            role_name=role_name,
            create_time=time_stamp,
            update_time=time_stamp,
            access=access_list
        )

        try:
            db.session.add(role)
            db.session.commit()
        except:
            db.session.rollback()
            raise AdminException('保存失败')

    def edit(self, role_name, access, id):
        role = self.query.filter_by(id=id).first()
        if not role:
            raise AdminException('角色不存在')
        role.role_name = role_name
        role.update_time = time.time()

        old_access = role.access.all()
        for access_item in old_access:
            # print(access_item)
            access_item.roles.remove(role)

        access_list = ManageAccess.query.filter(ManageAccess.id.in_(access)).all()
        for access in access_list:
            role.access.append(access)

        try:
            db.session.add(role)
            db.session.commit()
        except:
            db.session.rollback()
            raise AdminException('保存失败')

    def delete_role(self, role_id):
        role = self.query.filter_by(id=role_id).first()
        if not role:
            raise AdminException('角色不存在')

        # 判断角色下是还存在管理员
        if role.manages.count() > 0:
            raise AdminException('此角色下还存在管理员，不能删除')

        try:
            db.session.delete(role)
            db.session.commit()
        except:
            db.session.rollback()
            raise AdminException('删除失败')
