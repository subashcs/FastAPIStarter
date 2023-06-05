
"""create user table

Revision ID: 1
Revises: 
Create Date: 2021-11-20 19:17:01.434529

"""
from sqlalchemy.orm import Session
from app.orm.base import Base
from app.database.dbengine import engine
from app.orm.user import User, Phone


# revision identifiers, used by Alembic.
revision = '1'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)

    

    # create sample data
    user1 = User(id=1, name="Alice", fullname="Alice Com")
    db.add(user1)

    phone1 = Phone(id=1, phone_number="9832412736", user_id=1)
    db.add(phone1)
    
    user2 = User(id=2, name="Bob", fullname="Alice Com")
    db.add(user2)

    db.commit()

def downgrade():
    Base.metadata.drop_all(bind=engine)

