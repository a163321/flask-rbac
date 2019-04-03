from app.extension import db
from app.common import AdminException
import time


class ManageAccess(db.Model):
    __tablename__ = 'manage_access'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    access_name = db.Column(db.String(40), nullable=False)
    path = db.Column(db.String(200), index=True, nullable=True)
    parent_id = db.Column(db.Integer, index=True, default=0)
    create_time = db.Column(db.Integer, index=True, default=0)
    update_time = db.Column(db.Integer, index=True, default=0)

    def get_all_access(self):
        access = self.query.all()
        return access

    def get_select_access(self, access, parent_id=0, deep=1, temp_tree_list=[]):
        for item in access:
            if item.parent_id == parent_id:
                item_val = {
                    "id": item.id,
                    "deep": deep,
                    "name": item.access_name,
                    "path": item.path,
                    "create_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item.create_time))
                }
                temp_tree_list.append(item_val)
                self.get_select_access(access, item.id, deep + 1, temp_tree_list)

        return temp_tree_list

    def check_name_exist(self, name, id=0):
        if id:
            filters = {
                ManageAccess.access_name == name,
                ManageAccess.id != id
            }
        else:
            filters = {
                ManageAccess.access_name == name,
            }

        count = self.query.filter(*filters).count()
        return count

    def add_or_edit(self, access_name, path, parent_id=0, id=0):
        time_stamp = time.time()
        if not id:
            access = ManageAccess(access_name=access_name, parent_id=parent_id, path=path, create_time=time_stamp,
                                  update_time=time_stamp)
        else:
            access = self.query.filter_by(id=id).first()
            if not access:
                raise AdminException('对象不存在')

            access.access_name = access_name
            access.praent_id = parent_id
            access.path = path
            access.update_time = time_stamp

        try:
            db.session.add(access)
            db.session.commit()
        except:
            db.session.rollback()
            raise AdminException('保存失败')

    def delete_access(self, access_id):
        access = self.query.filter_by(id=access_id).first()
        if not access:
            raise AdminException('对象不存在')

        if access.roles.count() > 0:
            raise AdminException('存在角色使用了此权限，不能删除')

        try:
            db.session.delete(access)
            db.session.commit()
        except:
            db.session.rollback()
            raise AdminException('删除失败')
