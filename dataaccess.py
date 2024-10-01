import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry
from sqlalchemy.sql import func
from typing_extensions import Annotated

str_100 = Annotated[str, 100]

class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            str_100: String(100)
        }
    )

db = SQLAlchemy(model_class=Base)

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str_100] = mapped_column()
    body: Mapped[str_100] = mapped_column(nullable=True)
    completed: Mapped[bool] = mapped_column(default=False, index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now()
    )

class DbAccess:
    def get_all(self, hide_completed=False):
        query = Task.query
        if hide_completed:
            query = query.filter_by(completed=False)
        return query.all()
    
    def find_by_id(self, id):
        return Task.query.filter_by(id=id).one()
    
    def delete_all(self):
        Task.query.delete()
        db.session.commit()

    def create(self, task):
        db.session.add(task)
        db.session.commit()

    def update(self, task):
        Task.query \
            .filter_by(id=task.id) \
            .update({
                'title': task.title,
                'body': task.body,
                'completed': task.completed
            })
        db.session.commit()

    def delete(self, task):
        db.session.delete(task)
        db.session.commit()

    def delete_by_id(self, id):
        Task.query.filter_by(id=id).delete()
        db.session.commit()

def create_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return DbAccess()
