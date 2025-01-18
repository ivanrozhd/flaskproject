from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '4ed06c9a0ff2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # Check existing columns in the 'interests' table
    existing_columns = conn.execute(sa.text("PRAGMA table_info('interests');")).fetchall()
    column_names = [col[1] for col in existing_columns]

    # Add missing columns
    if 'id' not in column_names:
        with op.batch_alter_table('interests', schema=None) as batch_op:
            batch_op.add_column(sa.Column('id', sa.Integer(), nullable=True))
        conn.execute(sa.text("UPDATE interests SET id = rowid"))  # Populate 'id'
        with op.batch_alter_table('interests', schema=None) as batch_op:
            batch_op.alter_column('id', nullable=False)

    if 'hobby' not in column_names:
        with op.batch_alter_table('interests', schema=None) as batch_op:
            batch_op.add_column(sa.Column('hobby', sa.String(length=10), nullable=True))
        conn.execute(sa.text("UPDATE interests SET hobby = 'default'"))  # Provide default value
        with op.batch_alter_table('interests', schema=None) as batch_op:
            batch_op.alter_column('hobby', nullable=False)

    if 'user_id' not in column_names:
        with op.batch_alter_table('interests', schema=None) as batch_op:
            batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))

    # Add foreign key if not already present
    fk_constraints = conn.execute(sa.text("PRAGMA foreign_key_list('interests');")).fetchall()
    fk_names = [fk[2] for fk in fk_constraints]

    if 'user' not in fk_names:
        with op.batch_alter_table('interests', schema=None) as batch_op:
            batch_op.create_foreign_key('fk_interests_user_id', 'user', ['user_id'], ['id'])

    # Drop 'name' column if it exists
    if 'name' in column_names:
        with op.batch_alter_table('interests', schema=None) as batch_op:
            batch_op.drop_column('name')

def downgrade():
    with op.batch_alter_table('interests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=10), nullable=False))
        batch_op.drop_constraint('fk_interests_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')
        batch_op.drop_column('hobby')
        batch_op.drop_column('id')

    op.create_table('todo',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('content', sa.VARCHAR(length=200), nullable=False),
    sa.Column('completed', sa.INTEGER(), nullable=True),
    sa.Column('date_created', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
