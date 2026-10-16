from alembic import op
import sqlalchemy as sa

revision = "0003_campus_ticket_fields"
down_revision = "0002_create_tickets"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "tickets",
        sa.Column("category", sa.String(20), nullable=False, server_default="OTHER"),
    )
    op.add_column(
        "tickets",
        sa.Column(
            "location",
            sa.String(160),
            nullable=False,
            server_default="Legacy location unspecified",
        ),
    )


def downgrade():
    op.drop_column("tickets", "location")
    op.drop_column("tickets", "category")
