from app.models import db
from app import create_app

## Add when deploying
apps = create_app("ProductionConfig")
with apps.app_context():
    # db.drop_all()
    db.create_all()
