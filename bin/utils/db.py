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

import sys

sys.path.append("../")

import config
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime, timezone
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
    source = Column(String)
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


def db_init():
    # Create the engine and initialize the database
    print("Initializing database...")

    engine = create_engine(
        f"sqlite:///{config.DATABASE_LOCATION}/{config.DATABASE_NAME}.db",
        echo=False,
        pool_size=10,
        max_overflow=20,
    )
    print("Creating tables...")
    Base.metadata.create_all(engine)
    print("Database initialization complete.")
    # print location of database
    print(f"Database location: {config.DATABASE_LOCATION}/{config.DATABASE_NAME}.db")
    return engine


def db_get_engine():
    engine = create_engine(
        f"sqlite:///{config.DATABASE_LOCATION}/{config.DATABASE_NAME}.db",
        echo=False,
        pool_size=10,
        max_overflow=20,
    )
    return engine


def db_data_log_create(source, data, format):
    engine = db_get_engine()
    session = Session(bind=engine)
    print("Creating data log...")

    if format == "json":
        session.add(
            DataLogs(
                date=datetime.utcnow(), format=format, dataJSON=data, source=source
            )
        )
    elif format == "string":
        session.add(
            DataLogs(
                date=datetime.utcnow(), format=format, dataString=data, source=source
            )
        )
    else:
        pass
    session.commit()

    session.close()


def db_data_event_create(type, status, name, message, source):
    engine = db_get_engine()
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


def db_data_transmission_create(from_id, to_id, status):
    engine = db_get_engine()
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


def db_data_transmission_update(id, status):
    engine = db_get_engine()
    session = Session(bind=engine)
    session.query(dataTransmissions).filter(dataTransmissions.id == id).update(
        {"status": status, "updated_at": datetime.utcnow()}
    )
    session.commit()
    session.close()


def db_data_to_csv(table_name, file_path, from_id, to_id, source):
    engine = db_get_engine()
    with Session(bind=engine) as session:
        # Get the column names from the table
        columns = session.execute(text(f"SELECT * FROM {table_name} LIMIT 0")).keys()

        # Get the data from the table
        data = session.execute(
            text(f"SELECT * FROM {table_name} where id> {from_id} and id <= {to_id}")
        ).fetchall()

        # Write the data to a CSV file
        with open(file_path, "w", newline="") as csv_file:
            # add comment in first line
            writer = csv.writer(csv_file)
            dt = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
            dt = dt[:-2] + ":" + dt[-2:]
            writer.writerow([f"#pizero-serial={config.PIZERO_SERIAL}"])
            writer.writerow([f"#date={dt}"])
            writer.writerow([f"#data-logging-of={source}"])
            writer.writerow([f"#base-station-id={config.ID}"])
            writer.writerow([f"#base-station-location={config.SCHOOL_LOCATION}"])

            writer.writerow(columns)
            writer.writerows(data)


def db_last_row_data_transmission():
    engine = db_get_engine()
    with Session(bind=engine) as session:
        # Get the data from the table
        last_row = (
            session.query(dataTransmissions)
            .order_by(dataTransmissions.id.desc())
            .first()
        )
        return last_row


def db_get_dataLogs_length():
    engine = db_get_engine()
    with Session(bind=engine) as session:
        # Get the data from the table
        length = session.query(DataLogs).count()
        return length


def db_export_all_data_to_csv(name):
    engine = db_get_engine()
    with Session(bind=engine) as session:
        # Get the data from the table
        data = session.execute(text(f"SELECT * FROM dataLogs")).fetchall()
        name = name + ".csv"
        # Write the data to a CSV file
        with open(name, "w", newline="") as csv_file:
            # add comment in first line
            writer = csv.writer(csv_file)
            dt = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
            dt = dt[:-2] + ":" + dt[-2:]
            writer.writerow([f"#pizero-serial={config.PIZERO_SERIAL}"])
            writer.writerow([f"#date={dt}"])
            writer.writerow([f"#base-station-id={config.ID}"])
            writer.writerow([f"#base-station-location={config.SCHOOL_LOCATION}"])

            writer.writerow(
                ["id", "date", "format", "dataJSON", "dataString", "source"]
            )
            writer.writerows(data)

def db_show_data_from(from_id):
    engine = db_get_engine()
    with Session(bind=engine) as session:
        # Get the data from the table
        data = session.execute(
            text(f"SELECT * FROM dataLogs where id> {from_id}")
        ).fetchall()
        for d in data:
            print(d)


# db_init()
# for i in range(167):
#     print(i)
#     db_data_log_create(db_get_engine("test1"), "test", DataFormat.STRING)

# db_data_to_csv(db_get_engine("test1"), "datalogs", "test.csv", 0, 100)
