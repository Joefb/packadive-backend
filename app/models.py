from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Boolean, String, ForeignKey


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
    password: Mapped[str] = mapped_column(String(300), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # Relationship
    checklists: Mapped[list["CheckList"]] = relationship(
        "CheckList", back_populates="user"
    )
    trips: Mapped[list["Trip"]] = relationship("Trip", back_populates="user")


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    trip_name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="trips")
    checklists: Mapped[list["CheckList"]] = relationship(
        "CheckList", back_populates="trip", cascade="all, delete-orphan"
    )


class CheckList(Base):
    __tablename__ = "checklists"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    checklist_name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"), nullable=False)
    favorite: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="checklists")
    trip: Mapped["Trip"] = relationship("Trip", back_populates="checklists")
    list_items: Mapped[list["ListItems"]] = relationship(
        "ListItems", back_populates="checklist_items", cascade="all, delete-orphan"
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
