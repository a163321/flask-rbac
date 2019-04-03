from flask import Blueprint, render_template, request, url_for

blue_admin_user = Blueprint("blue_admin_user",
                            __name__,
                            url_prefix='/admin',
                            template_folder='../../../templates',
                            static_folder='../../../static'
                            )


@blue_admin_user.route('/user')
def user_index():
    return render_template('admin/user/index.html')
