from app.extensions import ma
from app.models import CheckList


class CheckListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CheckList


checklist_schema = CheckListSchema()
create_checklist_schema = CheckListSchema()
