from app.extensions import ma
from app.models import ListItems
from marshmallow import fields


class ListItemsSchema(ma.SQLAlchemyAutoSchema):
    checklist_id = fields.Int(required=True)

    class Meta:
        model = ListItems
        # load_instance = True


list_item_schema = ListItemsSchema()
create_list_item_schema = ListItemsSchema()
