from flask import Blueprint, render_template, request, url_for

blue_admin_content = Blueprint("blue_admin_content",
                               __name__,
                               url_prefix='/admin',
                               template_folder='../../../templates',
                               static_folder='../../../static'
                               )


@blue_admin_content.route('/content')
def content_index():
    return render_template('admin/content/index.html')
