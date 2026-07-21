from app.extensions import ma
from app.models import CheckList
from app.blueprints.list_item.schemas import ListItemsSchema
from marshmallow import fields


class CheckListSchema(ma.SQLAlchemyAutoSchema):
    list_items = fields.Nested(ListItemsSchema, many=True)
    trip_id = fields.Integer(required=True)
    # No route sets favorite yet (future favorite feature); keep it read-only
    # for now so it can't become a required/writable field by accident.
    favorite = fields.Boolean(dump_only=True)

    class Meta:
        model = CheckList


checklist_schema = CheckListSchema()
checklists_schema = CheckListSchema(many=True)
