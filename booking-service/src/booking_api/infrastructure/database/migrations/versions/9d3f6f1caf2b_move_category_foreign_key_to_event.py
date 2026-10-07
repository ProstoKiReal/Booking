"""move category foreign key to event

Revision ID: 9d3f6f1caf2b
Revises: 252554b6e1fd
Create Date: 2026-10-04 10:07:46.885276

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d3f6f1caf2b'
down_revision: Union[str, Sequence[str], None] = '252554b6e1fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('events', sa.Column('category_id', sa.Uuid(), nullable=True))
    op.create_foreign_key(
        'fk_events_category_id_categiries',
        'events',
        'categiries',
        ['category_id'],
        ['id'],
    )
    op.execute(
        """
        DO $$ BEGIN
            IF EXISTS (
                SELECT event_id
                FROM categiries
                GROUP BY event_id
                HAVING count(*) > 1
            ) THEN
                RAISE EXCEPTION 'Cannot migrate: an event has multiple categories';
            END IF;
        END $$;
        """
    )
    op.execute(
        """
        UPDATE events AS event
        SET category_id = category.id
        FROM categiries AS category
        WHERE category.event_id = event.id
        """
    )
    op.execute(
        """
        DO $$ BEGIN
            IF EXISTS (SELECT 1 FROM events WHERE category_id IS NULL) THEN
                RAISE EXCEPTION 'Cannot migrate: an event has no category';
            END IF;
        END $$;
        """
    )
    op.drop_constraint('categiries_event_id_fkey', 'categiries', type_='foreignkey')
    op.drop_column('categiries', 'event_id')
    op.alter_column('events', 'category_id', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('categiries', sa.Column('event_id', sa.Uuid(), nullable=True))
    op.create_foreign_key(
        'categiries_event_id_fkey',
        'categiries',
        'events',
        ['event_id'],
        ['id'],
    )
    op.execute(
        """
        DO $$ BEGIN
            IF EXISTS (
                SELECT category.id
                FROM categiries AS category
                LEFT JOIN events AS event ON event.category_id = category.id
                GROUP BY category.id
                HAVING count(event.id) <> 1
            ) THEN
                RAISE EXCEPTION 'Cannot downgrade: categories are unassigned or shared';
            END IF;
        END $$;
        """
    )
    op.execute(
        """
        UPDATE categiries AS category
        SET event_id = event.id
        FROM events AS event
        WHERE event.category_id = category.id
        """
    )
    op.alter_column('categiries', 'event_id', nullable=False)
    op.drop_constraint('fk_events_category_id_categiries', 'events', type_='foreignkey')
    op.drop_column('events', 'category_id')
