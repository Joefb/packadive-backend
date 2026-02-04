from app.extensions import ma
from app.models import CheckList


class CheckListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CheckList


check_list_schema = CheckListSchema()
create_check_list_schema = CheckListSchema()
