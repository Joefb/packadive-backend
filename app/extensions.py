from flask_marshmallow import Marshmallow  # Importing Marshmallow class
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache


# Create Marshmallow instance
ma = Marshmallow()
limiter = Limiter(get_remote_address, default_limits=["2000 per day", "500 per hour"])
cache = Cache()
