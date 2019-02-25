# app/models/department

from app import db

# The Department and Role models are quite similar. Both have name and description fields. Additionally, both have a
# one-to-many relationship with the Employee model (one department or role can have many employees). We define this in
# both models using the employees field. backref allows us to create a new property on the Employee model such that we
# can use employee.department or employee.role to get the department or role assigned to that employee. lazy defines how
# the data will be loaded from the database; in this case it will be loaded dynamically, which is ideal for managing
# large collections.

class Department(db.Model):
    """ Create a Department table """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department', lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)