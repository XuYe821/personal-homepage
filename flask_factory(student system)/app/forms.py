from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    id = IntegerField('Id') 
    name = StringField('Name',validators=[DataRequired()]) 
    # 新增 SelectField，coerce=int 确保表单返回的是整数ID
    major = SelectField('Major', coerce=int)
    submit = SubmitField('Submit') 
class EditForm(NameForm):
    submit = SubmitField("Edit") 
class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")