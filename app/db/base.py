from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models so they're registered with Base.metadata before create_all
# Do not remove these imports even if unused
try:
	from app.models.contact_model import Contact  # noqa: F401
	from app.models.contribute_model import Contribute  # noqa: F401
except Exception:
	# Safe import for tooling; runtime will import during app startup
	pass
