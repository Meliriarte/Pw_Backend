from peewee import *
import os

# Configuración de la base de datos
DATABASE_URL = os.environ.get('DATABASE_URL')

# Si no hay DATABASE_URL (desarrollo local), usar SQLite
if DATABASE_URL:
    # Producción con PostgreSQL
    db = PostgresqlDatabase(DATABASE_URL)
else:
    # Desarrollo local con SQLite
    db = SqliteDatabase('tasks.db')

class BaseModel(Model):
    class Meta:
        database = db

class Task(BaseModel):
    id = AutoField(primary_key=True)
    title = CharField(max_length=200)
    done = BooleanField(default=False)
    
    class Meta:
        table_name = 'tasks'

# Función para conectar y crear tablas
def initialize_db():
    db.connect()
    db.create_tables([Task], safe=True)
    
def close_db():
    if not db.is_closed():
        db.close()
