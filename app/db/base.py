from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models so they're registered with Base.metadata before create_all
# Do not remove these imports even if unused
try:
	from app.karlo_c.models.contact_model import Contact  # noqa: F401
	from app.karlo_c.models.contribute_model import Contribute  # noqa: F401
	from app.karlo_c.models.user_model import KarloUser  # noqa: F401
	from app.karlo_c.models.task_model import Task  # noqa: F401
	from app.karlo_c.models.user_settings_model import UserSettings  # noqa: F401
except Exception:
	# Safe import for tooling; runtime will import during app startup
	pass
