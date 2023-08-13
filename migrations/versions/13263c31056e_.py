"""empty message

Revision ID: 13263c31056e
Revises: 03920569c76a
Create Date: 2023-08-10 23:11:40.634504

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13263c31056e'
down_revision = '03920569c76a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people_details', schema=None) as batch_op:
        batch_op.add_column(sa.Column('height', sa.Integer(), nullable=True))
        batch_op.drop_column('heigth')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people_details', schema=None) as batch_op:
        batch_op.add_column(sa.Column('heigth', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_column('height')

    # ### end Alembic commands ###