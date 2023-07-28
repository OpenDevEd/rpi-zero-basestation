from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Enum,
    JSON,
    text,
)
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime
import enum
import csv

# Define the database schema
Base = declarative_base()

DATA_CHUNK_SIZE = 100


# create enum for data format
class DataFormat(enum.Enum):
    JSON = "json"
    STRING = "string"


class DataLogs(Base):
    __tablename__ = "dataLogs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.utcnow())
    format = Column(Enum(DataFormat))
    dataJSON = Column(JSON, nullable=True)
    dataString = Column(String, nullable=True)


class DataEvents(Base):
    __tablename__ = "dataEvents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.utcnow())
    type = Column(String)
    status = Column(String)
    name = Column(String)
    message = Column(String)
    source = Column(String)


class dataTransmissions(Base):
    __tablename__ = "dataTransmissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.utcnow())
    from_id = Column(Integer)
    to_id = Column(Integer)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())


def db_init(name):
    # Create the engine and initialize the database
    engine = create_engine(
        "sqlite:///{}.db".format(name), echo=False, pool_size=10, max_overflow=20
    )
    Base.metadata.create_all(engine)
    return engine


def db_get_engine(name):
    engine = create_engine(
        "sqlite:///{}.db".format(name), echo=False, pool_size=10, max_overflow=20
    )
    return engine


def db_data_log_create(engine, data, format):
    session = Session(bind=engine)
    if format == DataFormat.JSON:
        data_log = DataLogs(date=datetime.utcnow(), format=format, dataJSON=data)
    elif format == DataFormat.STRING:
        data_log = DataLogs(date=datetime.utcnow(), format=format, dataString=data)
    else:
        pass
    session.add(data_log)
    session.commit()
    session.close()


def db_data_event_create(engine, type, status, name, message, source):
    session = Session(bind=engine)
    session.add(
        DataEvents(
            date=datetime.utcnow(),
            type=type,
            status=status,
            name=name,
            message=message,
            source=source,
        )
    )
    session.commit()
    session.close()


def db_data_transmission_create(engine, from_id, to_id, status):
    session = Session(bind=engine)
    data_transmission = dataTransmissions(
        date=datetime.utcnow(), from_id=from_id, to_id=to_id, status=status
    )
    session.add(data_transmission)
    session.commit()
    data_transmission_id = data_transmission.id
    session.close()
    return data_transmission_id
    # return id


def db_data_transmission_update(engine, id, status):
    session = Session(bind=engine)
    session.query(dataTransmissions).filter(dataTransmissions.id == id).update(
        {"status": status, "updated_at": datetime.utcnow()}
    )
    session.commit()
    session.close()


def db_data_to_csv(engine, table_name, file_path, from_id, to_id):
    with Session(bind=engine) as session:
        # Get the column names from the table
        columns = session.execute(text(f"SELECT * FROM {table_name} LIMIT 0")).keys()

        # Get the data from the table
        data = session.execute(
            text(f"SELECT * FROM {table_name} where id> {from_id} and id <= {to_id}")
        ).fetchall()

        # Write the data to a CSV file
        with open(file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(columns)
            writer.writerows(data)


def db_last_row_data_transmission(engine):
    with Session(bind=engine) as session:
        # Get the data from the table
        last_row = (
            session.query(dataTransmissions)
            .order_by(dataTransmissions.id.desc())
            .first()
        )
        return last_row


def db_get_dataLogs_length(engine):
    with Session(bind=engine) as session:
        # Get the data from the table
        length = session.query(DataLogs).count()
        return length


db_init("test1")
for i in range(200):
    print(i)
    db_data_log_create(db_get_engine("test1"), "test", DataFormat.STRING)

db_data_to_csv(db_get_engine("test1"), "datalogs", "test.csv", 0, 100)
