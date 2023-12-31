"""empty message

Revision ID: 03920569c76a
Revises: 69471ba51679
Create Date: 2023-08-10 18:38:52.935259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03920569c76a'
down_revision = '69471ba51679'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('url', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('uid'),
    sa.UniqueConstraint('url')
    )
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('url', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('uid'),
    sa.UniqueConstraint('url')
    )
    op.create_table('vehicles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('url', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('uid'),
    sa.UniqueConstraint('url')
    )
    op.create_table('people_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('heigth', sa.Integer(), nullable=True),
    sa.Column('mass', sa.Integer(), nullable=True),
    sa.Column('hair_color', sa.String(length=50), nullable=True),
    sa.Column('skin_color', sa.String(length=50), nullable=True),
    sa.Column('eye_color', sa.String(length=50), nullable=True),
    sa.Column('birth_year', sa.String(length=30), nullable=True),
    sa.Column('gender', sa.String(length=30), nullable=True),
    sa.Column('homeworld', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['homeworld'], ['planets.uid'], ),
    sa.ForeignKeyConstraint(['uid'], ['people.uid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people_favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_people', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_people'], ['people.uid'], ),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planet_favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_planet', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_planet'], ['planets.uid'], ),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planets_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('diameter', sa.Integer(), nullable=True),
    sa.Column('rotation_period', sa.Integer(), nullable=True),
    sa.Column('orbital_period', sa.Integer(), nullable=True),
    sa.Column('gravity', sa.String(length=50), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('climate', sa.String(length=50), nullable=True),
    sa.Column('terrain', sa.String(length=30), nullable=True),
    sa.Column('surface_water', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['planets.uid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vehicles_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('model', sa.String(length=50), nullable=True),
    sa.Column('vehicle_class', sa.String(length=50), nullable=True),
    sa.Column('manufacturer', sa.String(length=50), nullable=True),
    sa.Column('cost_in_credits', sa.Integer(), nullable=True),
    sa.Column('length', sa.Float(), nullable=True),
    sa.Column('crew', sa.Integer(), nullable=True),
    sa.Column('passengers', sa.Integer(), nullable=True),
    sa.Column('max_atmosphering_speed', sa.Integer(), nullable=True),
    sa.Column('consumables', sa.String(length=30), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['vehicles.uid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vehicles_favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_vehicle', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ),
    sa.ForeignKeyConstraint(['id_vehicle'], ['vehicles.uid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('is_active',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('is_active',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    op.drop_table('vehicles_favorites')
    op.drop_table('vehicles_details')
    op.drop_table('planets_details')
    op.drop_table('planet_favorites')
    op.drop_table('people_favorites')
    op.drop_table('people_details')
    op.drop_table('vehicles')
    op.drop_table('planets')
    op.drop_table('people')
    # ### end Alembic commands ###
