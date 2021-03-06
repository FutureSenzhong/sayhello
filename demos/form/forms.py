from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, MultipleFileField, \
    TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError


# 如果你想手动编写HTML表单的代码，要注意表单字段的name属性
# 值必须和表单类的字段名称相同，这样在提交表单时WTForms才能正确
# 地获取数据并进行验证
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('Remember me', default=True)
    submit = SubmitField('Log in')


# 设置内置错误消息语言为中文
class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']


class HelloForm(MyBaseForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField()


# 自定义验证器（行内验证器）
class FortyTwoForm(FlaskForm):
    answer = IntegerField('The Number')
    submit = SubmitField()

    @classmethod
    def validate_answer(cls, field):
        if field.data != 42:
            raise ValidationError('Must be 42.')


# 自定义验证器（全局验证器）没有参数的全局函数验证器
# def is_42(form, field):
#     if field.data != 42:
#         raise ValidationError('Must be 42')
#
#
# class FortyTwoForm(FlaskForm):
#     answer = IntegerField('The Number', validators=[is_42])
#     submit = SubmitField()


# 自定义验证器（全局验证器）有参数的全局函数验证器（工厂函数）
def is_42(message=None):
    if message is None:
        message = 'Must be 42.'

    def _is_42(form, field):
        if field.data != 42:
            raise ValidationError(message)
    return _is_42


class FortyTwoForm1(FlaskForm):
    answer = IntegerField('The Number', validators=[is_42()])
    submit = SubmitField()


# 类验证器
# class Length(object):
#     def __init__(self, min=-1, max=-1, message=None):
#         self.min = min
#         self.max = max
#         if not message:
#             message = u'Field must be between %i and %i characters long.' % (min, max)
#         self.message = message
#
#     def __call__(self, form, field):
#         l = field.data and len(field.data) or 0
#         if l < self.min or self.max != -1 and l > self.max:
#             raise ValidationError(self.message)
# length = Length

# 文件上传
# CSRF
# 验证文件类型
# 验证文件大小
# 过滤文件名
class UploadForm(FlaskForm):
    # 单个上传
    photo = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])

    # 批量上传
    # photo = MultipleFileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField()


class MultiUploadForm(FlaskForm):
    # 单个上传
    # photo = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])

    # 批量上传
    photo = MultipleFileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    submit = SubmitField()


# 创建富文本表单类
class RichTextForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 50)])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Publish')


class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 50)])
    body = TextAreaField('Body', validators=[DataRequired()])
    save = SubmitField('Save') # 保存按钮
    publish = SubmitField('Publish') # 发布按钮