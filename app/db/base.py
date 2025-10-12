from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models so they're registered with Base.metadata before create_all
# Do not remove these imports even if unused
try:
	from app.models.contact_model import Contact  # noqa: F401
	from app.models.contribute_model import Contribute  # noqa: F401
	from app.models.user_model import User  # noqa: F401
	
	# Home Cure models
	from app.home_cure.models.user_model import User as HomeCureUser  # noqa: F401
	from app.home_cure.models.service_model import Service  # noqa: F401
	from app.home_cure.models.contact_model import Contact as HomeCureContact  # noqa: F401
	from app.home_cure.models.technician_model import Technician  # noqa: F401
	from app.home_cure.models.booking_model import Booking  # noqa: F401
	from app.home_cure.models.health_record_model import HealthRecord  # noqa: F401
	from app.home_cure.models.technician_earnings_model import TechnicianEarnings  # noqa: F401
	from app.home_cure.models.admin_log_model import AdminLog  # noqa: F401
	from app.home_cure.models.system_settings_model import SystemSettings  # noqa: F401
	from app.home_cure.models.notification_model import Notification  # noqa: F401
except Exception:
	# Safe import for tooling; runtime will import during app startup
	pass
