from flask import Blueprint, render_template, request, url_for
from app.models import ManageAccess, ManageRole, ManageUser
from app.forms.admin import AccessForm, RoleForm, ManageForm
from app.common import AdminException, Tool

blue_admin_manage = Blueprint("blue_admin_manage",
                              __name__,
                              url_prefix='/admin',
                              template_folder='../../../templates',
                              static_folder='../../../static'
                              )


# 管理员列表
@blue_admin_manage.route('/manage')
def manage_index():
    list = ManageUser.query.all()
    for item in list:
        roles = item.roles.all()
        role_names = []
        for role in roles:
            role_names.append(role.role_name)
        item.create_time = Tool.format_time(item.create_time)
        item.role_names = ','.join(role_names) if len(role_names) > 0 else ''
    return render_template('admin/manage/index.html', list=list)


@blue_admin_manage.route('/manage/add', methods=['GET', 'POST'])
def manage_add():
    forms = ManageForm()
    if request.method == 'POST':
        validate = forms.validate()
        if not validate:
            error = Tool.get_error(forms.errors)
            return Tool.admin_json_response(message=error, code=0)

        role_ids = request.form.getlist('role_id[]')
        try:
            forms.save(role_id=role_ids)

            return Tool.admin_json_response('保存成功', url=url_for('blue_admin_manage.manage_index'))
        except AdminException as e:
            return Tool.admin_json_response(message=e.message, code=0)

    # 获取全部角色
    roles = ManageRole.query.all()
    return render_template('admin/manage/manage_add.html', roles=roles, forms=forms)


@blue_admin_manage.route('/manage/edit', methods=['GET', 'POST'])
def manage_edit():
    forms = ManageForm()
    if request.method == 'POST':
        validate = forms.validate()
        if not validate:
            error = Tool.get_error(forms.errors)
            return Tool.admin_json_response(message=error, code=0)

        role_ids = request.form.getlist('role_id[]')
        try:
            forms.save(role_id=role_ids)

            return Tool.admin_json_response('保存成功', url=url_for('blue_admin_manage.manage_index'))
        except AdminException as e:
            return Tool.admin_json_response(message=e.message, code=0)

    id = request.args.get('id', 0)
    info = ManageUser.query.filter_by(id=id).first_or_404()
    roles = ManageRole.query.all()
    user_roles = info.roles.all()
    role_ids = []
    for user_role in user_roles:
        role_ids.append(user_role.id)
    return render_template('admin/manage/manage_edit.html', roles=roles, info=info, role_ids=role_ids, forms=forms)


@blue_admin_manage.route('/manage/delete', methods=['POST'])
def manage_delete():
    modal = ManageUser()
    id = int(request.form.get('user_id'))

    try:
        modal.delete_user(user_id=id)
        return Tool.admin_json_response(message="删除成功")
    except AdminException as e:
        return Tool.admin_json_response(message=e.message, code=0)


@blue_admin_manage.route('/role')
def role_index():
    list = ManageRole.query.all()
    for item in list:
        item.create_time = Tool.format_time(item.create_time)
    return render_template('admin/manage/role.html', list=list)


@blue_admin_manage.route('/role/add', methods=['GET', 'POST'])
def role_add():
    modal = ManageRole()
    form = RoleForm()
    if request.method == 'POST':
        validate = form.validate()
        if not validate:
            error = Tool.get_error(form.errors)
            return Tool.admin_json_response(message=error, code=0)

        role_name = request.form.get('role_name')
        access = request.form.getlist('access[]')

        try:
            form.save(role_name, access)

            return Tool.admin_json_response('保存成功', url=url_for('blue_admin_manage.role_index'))
        except AdminException as e:
            return Tool.admin_json_response(message=e.message, code=0)

    access = modal.get_all_access()
    return render_template('admin/manage/role_add.html', access=access, form=form)


@blue_admin_manage.route('/role/edit', methods=['GET', 'POST'])
def role_edit():
    modal = ManageRole()
    form = RoleForm()
    role_id = request.args.get('role_id', 0)
    if request.method == 'POST':
        validate = form.validate()
        if not validate:
            error = Tool.get_error(form.errors)
            return Tool.admin_json_response(message=error, code=0)

        role_name = request.form.get('role_name')
        access = request.form.getlist('access[]')

        try:
            form.save(role_name, access, id=role_id)

            return Tool.admin_json_response('保存成功', url=url_for('blue_admin_manage.role_index'))
        except AdminException as e:
            return Tool.admin_json_response(message=e.message, code=0)

    access = modal.get_all_access(role_id)
    info = ManageRole.query.filter_by(id=role_id).first_or_404()
    return render_template('admin/manage/role_edit.html', access=access, form=form, info=info)


@blue_admin_manage.route('/role/delete', methods=['POST'])
def role_delete():
    modal = ManageRole()
    id = int(request.form.get('role_id'))

    try:
        modal.delete_role(role_id=id)
        return Tool.admin_json_response(message="删除成功")
    except AdminException as e:
        return Tool.admin_json_response(message=e.message, code=0)


@blue_admin_manage.route('/access')
def access_index():
    modal = ManageAccess()
    all_access = modal.get_all_access()
    access = []
    if all_access:
        access = modal.get_select_access(all_access, temp_tree_list=[])

    return render_template('admin/manage/access.html', access=access)


@blue_admin_manage.route('/access/add', methods=['GET', 'POST'])
def access_add():
    modal = ManageAccess()
    access_form = AccessForm()
    if request.method == 'POST':
        validate = access_form.validate()
        if not validate:
            error = Tool.get_error(access_form.errors)
            return Tool.admin_json_response(message=error, code=0)

        try:
            access_form.save()
            url = url_for('blue_admin_manage.access_index')
            return Tool.admin_json_response(message="保存成功", url=url)
        except AdminException as e:
            return Tool.admin_json_response(message=e.message, code=0)

    all_access = modal.get_all_access()
    select_access = []
    if all_access:
        select_access = modal.get_select_access(all_access, temp_tree_list=[])

    return render_template('admin/manage/access_add.html', select_access=select_access, form=access_form)


@blue_admin_manage.route('/access/edit', methods=['GET', 'POST'])
def access_edit():
    modal = ManageAccess()
    access_form = AccessForm()
    if request.method == 'POST':
        validate = access_form.validate()
        if not validate:
            error = Tool.get_error(access_form.errors)
            return Tool.admin_json_response(message=error, code=0)

        try:
            access_form.save()
            url = url_for('blue_admin_manage.access_index')
            return Tool.admin_json_response(message="保存成功", url=url)
        except AdminException as e:
            return Tool.admin_json_response(message=e.message, code=0)

    id = request.args.get('id', 0)
    info = ManageAccess.query.filter_by(id=id).first_or_404()

    all_access = modal.get_all_access()
    select_access = []
    if all_access:
        select_access = modal.get_select_access(all_access, temp_tree_list=[])

    return render_template('admin/manage/access_edit.html', select_access=select_access, form=access_form, info=info)


@blue_admin_manage.route('/access/delete', methods=['POST'])
def access_delete():
    modal = ManageAccess()
    id = int(request.form.get('access_id'))

    try:
        modal.delete_access(access_id=id)
        return Tool.admin_json_response(message="删除成功")
    except AdminException as e:
        return Tool.admin_json_response(message=e.message, code=0)
