admin_menu = {
    "blue_admin_index": {
        "title": '首页',
        "url": '/admin',
        "icon": 'icon-home'
    },
    "blue_admin_manage": {
        "title": '管理员',
        "url": '/admin/manage',
        "icon": 'icon-guanliyuan',
        "children": [
            {
                "title": "管理员列表",
                "url": '/admin/manage',
                "uris": [
                    '/admin/manage',
                    '/admin/manage/add',
                    '/admin/manage/edit',
                    '/admin/manage/delete'
                ]
            },
            {
                "title": "角色列表",
                "url": '/admin/role',
                "uris": [
                    '/admin/role',
                    '/admin/role/add',
                    '/admin/role/edit',
                    '/admin/role/delete',
                ]
            },
            {
                "title": "权限列表",
                "url": '/admin/access',
                "uris": [
                    '/admin/access',
                    '/admin/access/add',
                    '/admin/access/edit',
                    '/admin/access/delete',
                ]
            }
        ]
    },
    "blue_admin_user": {
        "title": '用户管理',
        "url": '/admin/user',
        "icon": 'icon-user',
        "children": [
            {
                "title": "用户列表",
                "url": '/admin/user',
                "uris": [
                    '/admin/user',
                    '/admin/user/add',
                    '/admin/user/edit',
                    '/admin/user/delete'
                ]
            }
        ]
    },
    "blue_admin_content": {
        "title": '内容管理',
        "url": '/admin/content',
        "icon": 'am-icon-file',
        "children": [
            {
                "title": "文章列表",
                "url": '/admin/content',
                "uris": [
                    '/admin/content',
                    '/admin/content/add',
                    '/admin/content/edit',
                    '/admin/content/delete'
                ]
            },
            {
                "title": "公告列表",
                "url": '/admin/notice',
                "uris": [
                    '/admin/notice',
                    '/admin/notice/add',
                    '/admin/notice/edit',
                    '/admin/notice/delete'
                ]
            },
            {
                "title": "轮播图列表",
                "url": '/admin/banner',
                "uris": [
                    '/admin/banner',
                    '/admin/banner/add',
                    '/admin/banner/edit',
                    '/admin/banner/delete'
                ]
            }
        ]
    },
    "blue_admin_setting": {
        "title": '设置',
        "url": '/admin/setting',
        "icon": 'icon-setting',
        "children": [
            {
                "title": "基本配置",
                "url": '/admin/setting',
                "uris": [
                    '/admin/setting',
                    '/admin/setting/edit',
                ]
            },
        ]
    },
}


def getSubMenu(buleName):
    if buleName in admin_menu.keys():
        menus = admin_menu.get(buleName)
        sub_menus = menus.get('children')
        sub_menus = sub_menus if sub_menus else []

        return sub_menus, menus.get('title')
    else:
        return None
