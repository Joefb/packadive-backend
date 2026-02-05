from app.models import db
from app import create_app

apps = create_app("DevelopmentConfig")
with apps.app_context():
    # db.drop_all()
    db.create_all()

## Will take out when deploying
if __name__ == "__main__":
    apps.run()

## Add when deploying
# apps = create_app("DevelopmentConfig")
# with apps.app_context():
#     # db.drop_all()
#     db.create_all()
