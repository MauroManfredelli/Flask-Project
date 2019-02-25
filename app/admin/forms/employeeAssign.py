# app/admin/forms/employeeAssign.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
# We have imported a new field type, QuerySelectField, which we use for both the department and role fields. This will
# query the database for all departments and roles. The admin user will select one department and one role using the
# form on the front-end.
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ...models.department import Department
from ...models.role import Role


class EmployeeAssignForm(FlaskForm):
    """ Form for admin to assign departments and roles to employees """
    department = QuerySelectField(query_factory=lambda: Department.query.all(), get_label='name')
    role = QuerySelectField(query_factory=lambda: Role.query.all(), get_label='name')
    submit = SubmitField('Submit')