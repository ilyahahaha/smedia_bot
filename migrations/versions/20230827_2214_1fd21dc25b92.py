"""pause

Revision ID: 1fd21dc25b92
Revises: e959e88268ed
Create Date: 2023-08-27 22:14:38.835686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1fd21dc25b92'
down_revision: Union[str, None] = 'e959e88268ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_apscheduler_jobs_next_run_time', table_name='apscheduler_jobs')
    op.drop_table('apscheduler_jobs')
    op.add_column('user', sa.Column('is_paused', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.create_unique_constraint(None, 'user', ['user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'is_paused')
    op.create_table('apscheduler_jobs',
    sa.Column('id', sa.VARCHAR(length=191), autoincrement=False, nullable=False),
    sa.Column('next_run_time', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('job_state', postgresql.BYTEA(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='apscheduler_jobs_pkey')
    )
    op.create_index('ix_apscheduler_jobs_next_run_time', 'apscheduler_jobs', ['next_run_time'], unique=False)
    # ### end Alembic commands ###
