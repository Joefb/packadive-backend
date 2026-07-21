from app.extensions import ma
from app.models import Trip


class TripSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trip


trip_schema = TripSchema()
trips_schema = TripSchema(many=True)
