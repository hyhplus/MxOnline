# coding: utf-8
__author__ = 'Evan'

import xadmin

from xadmin import views
from users.models import EmailVerifyRecord, Banner


class EmailVerifyRecordAdmin(object):
    """
    邮箱验证码 X-admin 后台管理器

    X-admin 中这里是继承object，不再是继承admin
    # 显示的列                  list_display
    # 搜索字段，不要添加时间搜索   search_fields
    # 过滤                     list_filter
    """
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    """
    轮播图后台管理器
    # 显示的列   list_display
    # 搜索字段   search_fields
    # 过滤      list_filter
    """
    list_display = ['title', 'image', 'url','index', 'add_time']
    search_fields = ['title', 'image', 'url','index']
    list_filter = ['title', 'image', 'url','index', 'add_time']


class BaseSetting(object):
    """
    创建X-admin的全局管理器
    开启主题功能
    """
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    """
    X-admin 全局配置参数信息设置
    """
    site_title = 'MxOnline在线教育系统后台管理'
    site_footer = "Evan's demo"

    # 收起菜单
    # menu_style = 'accordion'


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)

# 将全局配置管理与view绑定注册
xadmin.site.register(views.BaseAdminView, BaseSetting)

# 将头部与脚部信息进行注册
xadmin.site.register(views.CommAdminView, GlobalSettings)