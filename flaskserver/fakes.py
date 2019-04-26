# -*- coding: utf-8 -*-

import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from flaskserver import db
from flaskserver.models import Admin,Admission

fake = Faker()

def fake_admin():
    admin = Admin(
        username='admin'
    )
    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()

def fake_admission():
    admission = Admission(
        school='中南大学',
        rank=3000,
        year=2015,
        kind='理科',
        grade=604,
        clazz='一本'
    )
    db.session.add(admission)
    db.session.commit()
