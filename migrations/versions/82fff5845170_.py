"""empty message

Revision ID: 82fff5845170
Revises: 794ee6b32465
Create Date: 2023-08-12 03:59:30.499612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82fff5845170'
down_revision = '794ee6b32465'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('people_details', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['uid'])

    with op.batch_alter_table('planets_details', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['uid'])

    with op.batch_alter_table('vehicles_details', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['uid'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vehicles_details', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('planets_details', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('people_details', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###