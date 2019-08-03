"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""
from lin import manager
from lin.exception import ParameterException
from wtforms import DateTimeField, PasswordField, FieldList, IntegerField, StringField
from wtforms.validators import DataRequired, Regexp, EqualTo, length, Optional, NumberRange
import time

from lin.forms import Form

from app.models.member import Member


# 注册校验
class RegisterForm(Form):
    password = PasswordField('新密码', validators=[
        DataRequired(message='新密码不可为空'),
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$', message='密码长度必须在6~22位之间，包含字符、数字和 _ '),
        EqualTo('confirm_password', message='两次输入的密码不一致，请输入相同的密码')])
    confirm_password = PasswordField('确认新密码', validators=[DataRequired(message='请确认密码')])
    nickname = StringField(validators=[DataRequired(message='昵称不可为空'),
                                       length(min=2, max=10, message='昵称长度必须在2~10之间')])

    group_id = IntegerField('分组id',
                            validators=[DataRequired(message='请输入分组id'), NumberRange(message='分组id必须大于0', min=1)])
    email = StringField('电子邮件', validators=[
        Regexp(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', message='电子邮箱不符合规范，请输入正确的邮箱'),
        Optional()
    ])

    def validate_group_id(self, value):
        exists = manager.group_model.get(id=value.data)
        if not exists:
            raise ValueError('分组不存在')


# 登陆校验
class LoginForm(Form):
    nickname = StringField(validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(message='密码不可为空')])


# 重置密码校验
class ResetPasswordForm(Form):
    new_password = PasswordField('新密码', validators=[
        DataRequired(message='新密码不可为空'),
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$', message='密码长度必须在6~22位之间，包含字符、数字和 _ '),
        EqualTo('confirm_password', message='两次输入的密码不一致，请输入相同的密码')
    ])
    confirm_password = PasswordField('确认新密码', validators=[DataRequired(message='请确认密码')])


# 更改密码校验
class ChangePasswordForm(ResetPasswordForm):
    old_password = PasswordField('原密码', validators=[DataRequired(message='不可为空')])


# 管理员创建分组
class NewGroup(Form):
    # 分组name
    name = StringField(validators=[DataRequired(message='请输入分组名称')])
    # 非必须
    info = StringField(validators=[Optional()])
    # 必填，分组的权限
    auths = FieldList(StringField(validators=[DataRequired(message='请输入auths字段')]))


# 管理员更新分组
class UpdateGroup(Form):
    # 分组name
    name = StringField(validators=[DataRequired(message='请输入分组名称')])
    # 非必须
    info = StringField(validators=[Optional()])


class DispatchAuths(Form):
    # 为用户分配的权限
    group_id = IntegerField('分组id',
                            validators=[DataRequired(message='请输入分组id'), NumberRange(message='分组id必须大于0', min=1)])
    auths = FieldList(StringField(validators=[DataRequired(message='请输入auths字段')]))


class DispatchAuth(Form):
    # 为用户分配的权限
    group_id = IntegerField('分组id',
                            validators=[DataRequired(message='请输入分组id'), NumberRange(message='分组id必须大于0', min=1)])
    # 用户查询自己信息
    auth = StringField(validators=[DataRequired(message='请输入auth字段')])


# 批量删除权限
class RemoveAuths(Form):
    group_id = IntegerField('分组id',
                            validators=[DataRequired(message='请输入分组id'), NumberRange(message='分组id必须大于0', min=1)])
    auths = FieldList(StringField(validators=[DataRequired(message='请输入auths字段')]))


# 日志查找范围校验
class LogFindForm(Form):
    # name可选，若无则表示全部
    name = StringField(validators=[Optional()])
    # 2018-11-01 09:39:35
    start = DateTimeField(validators=[])
    end = DateTimeField(validators=[])

    def validate_start(self, value):
        if value.data:
            try:
                _ = time.strptime(value.data, '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                raise e

    def validate_end(self, value):
        if value.data:
            try:
                _ = time.strptime(value.data, '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                raise e


class EventsForm(Form):
    group_id = IntegerField('分组id',
                            validators=[DataRequired(message='请输入分组id'), NumberRange(message='分组id必须大于0', min=1)])
    events = FieldList(StringField(validators=[DataRequired(message='请输入events字段')]))


# 更新用户邮箱
class UpdateInfoForm(Form):
    email = StringField('电子邮件', validators=[
        Regexp(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', message='电子邮箱不符合规范，请输入正确的邮箱'),
        Optional()
    ])


# 更新用户信息
class UpdateUserInfoForm(Form):
    group_id = IntegerField('分组id',
                            validators=[DataRequired(message='请输入分组id'), NumberRange(message='分组id必须大于0', min=1)])
    email = StringField('电子邮件', validators=[
        Regexp(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', message='电子邮箱不符合规范，请输入正确的邮箱'),
        Optional()
    ])


class BookSearchForm(Form):
    q = StringField(validators=[DataRequired(message='必须传入搜索关键字')])  # 前端的请求参数中必须携带`q`


class CreateOrUpdateBookForm(Form):
    title = StringField(validators=[DataRequired(message='必须传入图书名')])
    author = StringField(validators=[DataRequired(message='必须传入图书作者')])
    summary = StringField(validators=[DataRequired(message='必须传入图书综述')])
    image = StringField(validators=[DataRequired(message='必须传入图书插图')])

# 会员
class MemberSearchForm(Form):
    keyword = StringField(validators=[Optional(), DataRequired(message='必须传入搜索关键字'),
                                length(min=2, max=11, message='搜索关键字长度必须是2-11位数字或汉字'),
                                Regexp(r'^[\u4E00-\u9FA50-9]{2,11}$', message='请输入正确的搜索关键字、数字或汉字'),
                                ])  # 前端的请求参数中必须携带`q`
    # name可选，若无则表示全部
    lnput = StringField(validators=[Optional()])
    # 2018-11-01 09:39:35
    start = DateTimeField(validators=[])
    end = DateTimeField(validators=[])

class CreateOrUpdateMemberForm(Form):
    number_id = StringField(validators=[DataRequired(message='必须传入会员号'),
                                        length(min=8, max=8, message='会员号长度必须是8位'),
                                        Regexp(r'^\d{8}$', message='请输入正确的会员号'),
                                        ])
    name = StringField(validators=[DataRequired(message='必须传入姓名'),
                                   length(min=2, max=5, message='姓名长度必须是2-5位'),
                                   Regexp(r'^[\u4e00-\u9fa5]{2,5}$', message='请输入正确的姓名'),
                                   ])
    number = StringField(validators=[DataRequired(message='必须传入身份证号'),
                                     # length(min=10, max=18, message='身份证号长度必须是11位'),
                                     ])
    phone = StringField(validators=[DataRequired(message='必须传入手机号'),
                                    length(min=11, max=11, message='手机长度必须是11位'),
                                    Regexp(r'^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}$', message='请输入正确的手机号'),
                                    ])
    address = StringField(validators=[DataRequired(message='必须传入地址'),
                                      Regexp(r'^[\u4E00-\u9FA5A-Za-z0-9]+$', message='请输入正确的地址'),
                                      ])
    nation = StringField(validators=[DataRequired(message='必须传入民族'),
                                     length(min=2, max=8, message='民族长度必须是2-5位'),
                                     Regexp(r'^[\u4e00-\u9fa5]{2,8}$', message='请输入正确的民族'),
                                     ])
    birthday = StringField(validators=[DataRequired(message='必须传入生日')])
    remarks = StringField(validators=[DataRequired(message='必须传入备注')])
    lnput = StringField(validators=[DataRequired(message='必须传入输入人')])


    def validate_number_id(self, number_id):
        if Member.query.filter_by(number_id=number_id.data).filter(Member.delete_time == None).first():
            raise ParameterException('会员号已被注册')

    def validate_phone(self, phone):
        if Member.query.filter_by(phone=phone.data).filter(Member.delete_time == None).first():
            raise ParameterException('手机号已被注册')

    # hotel_id = IntegerField(validators=[Regexp(r'^\d{1,5}$', message="hotel_id必须是数字1-5位"), Optional()])


class CreateOrUpdateLnputForm(Form):
    name = StringField(validators=[DataRequired(message='必须传入姓名'),
                                   length(min=2, max=5, message='姓名长度必须是2-5位'),
                                   Regexp(r'^[\u4e00-\u9fa5]{2,5}$', message='请输入正确的姓名'),
                                   ])
    position = StringField(validators=[Optional()])
