from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey, Table, Column, Date
## from datetime import date


# Create a base class for our models
class Base(DeclarativeBase):
    pass


# Create a instance of the database
db = SQLAlchemy(model_class=Base)


## MODELS ##
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # Relationship
    checklists: Mapped[list["CheckList"]] = relationship(
        "CheckList", back_populates="user"
    )


class CheckList(Base):
    __tablename__ = "checklists"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    checklist_name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="checklists")
    list_items: Mapped[list["ListItems"]] = relationship(
        "ListItems", back_populates="checklist_items"
    )


class ListItems(Base):
    __tablename__ = "list_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    item_name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    checklist_id: Mapped[int] = mapped_column(
        ForeignKey("checklists.id"), nullable=False
    )

    # Relationship
    checklist_items: Mapped["CheckList"] = relationship(
        "CheckList", back_populates="list_items"
    )
