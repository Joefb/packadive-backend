from app.extensions import ma
from app.models import CheckList
from app.blueprints.list_item.schemas import ListItemsSchema
from marshmallow import fields


class CheckListSchema(ma.SQLAlchemyAutoSchema):
    # list_items = fields.Nested(ListItemsSchema, many=True, dump_only=True)
    list_items = fields.Nested(ListItemsSchema, many=True)

    class Meta:
        model = CheckList


checklist_schema = CheckListSchema()
checklists_schema = CheckListSchema(many=True)
create_checklist_schema = CheckListSchema()
