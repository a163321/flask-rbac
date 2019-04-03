from flask import request, g, session, redirect, url_for, abort
from app.models import ManageUser
from app.common import admin_menu, getSubMenu, Tool

no_require_path = ["/admin/login"]
no_auth_path = ["/admin", "/admin/", "/admin/logout"]


def check_login(app):
    @app.before_request
    def before_request():
        path = request.path

        if path not in no_require_path and not path.startswith('/admin/static/'):
            admin_id = session.get('admin_id')
            if not admin_id:
                return redirect(url_for('blue_admin_index.login'))

            # g.admin_id = admin_id 查询用户
            user_info = ManageUser.query.filter_by(id=admin_id).first()
            if not user_info or user_info.status != 1:
                return redirect(url_for('blue_admin_index.login'))

            # 判断权限
            access_paths = no_auth_path
            modal = ManageUser()
            get_access_paths = modal.get_manage_access(user_info)
            access_paths = access_paths + get_access_paths
            g.access_paths = access_paths
            g.admin_user_info = user_info
            if not user_info.is_super and path not in no_auth_path:
                if path not in access_paths:
                    # 没有权限，跳转到 错误页面
                    if request.is_xhr:
                        return Tool.admin_json_response('没有权限')
                    else:
                        abort(403)


def before_response(app):
    @app.context_processor
    def my_context_processor():
        path = request.path
        if path not in no_require_path:
            admin_user_info = g.admin_user_info
            if admin_user_info:
                # 获取menu菜单
                result = getSubMenu(request.blueprint)
                result = result if result else None
                sub_menus = result[0] if result else []
                menus_tile = result[1] if result else None

                access_paths = g.access_paths if hasattr(g, 'access_paths') and g.access_paths else []
                print(g.access_paths)
                return {
                    "username": admin_user_info.username,
                    "is_super": admin_user_info.is_super,
                    "menus": admin_menu,
                    "current_path": path,
                    "sub_menus": sub_menus,
                    "menus_title": menus_tile,
                    "blue_print": request.blueprint,
                    "access_paths": access_paths
                }
            else:
                return {}
        else:
            return {}
