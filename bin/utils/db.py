import csv
import enum
from datetime import datetime, timezone
from sqlalchemy.orm import declarative_base, Session
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
    print(f"Database location: {config.DATABASE_LOCATION}/{config.DATABASE_NAME}.db")
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



def run_sql_query(sql_query):
    engine = db_get_engine()
    session = Session(bind=engine)
    sql_query = text(sql_query)
    results = session.execute(sql_query).fetchall()
    session.close()
    return results


def get_last_datalog_by_source(filename):
    # Connect to the database
    sql_query = """
        SELECT id, date, json_extract(dataJSON, '$.topic') as 'topic', source, format, json_extract(dataJSON, '$.battery') as 'battery', json_extract(dataJSON, '$.temperature') as 'temperature'
        FROM dataLogs
        WHERE id IN (
            SELECT MAX(id)
            FROM dataLogs
            WHERE source = 'zigbee'
            GROUP BY json_extract(dataJSON, '$.topic')
        )
        ORDER BY id DESC;
    """
    results = run_sql_query(sql_query)
    with open(f"{filename}.txt", "w") as f:
        f.write("ID,Date,Topic,Source,Format,Battery,Temperature\n")
        for row in results:
            f.write(",".join(str(x) for x in row) + "\n")

    sql_query = """
        SELECT id, date, source, format, dataJSON, dataString
        FROM dataLogs
        WHERE id IN (
            SELECT MAX(id)
            FROM dataLogs
            WHERE source != 'zigbee' AND source != 'sensorboard-pm' AND source != 'sensorboard'
            GROUP BY source
        )
        ORDER BY id DESC;
    """
    results2 = run_sql_query(sql_query)
    with open(f"{filename}.txt", "a") as f:
        f.write("\nID,Date,Source,Format,DataJSON,DataString\n")
        for row in results2:
            f.write(",".join(str(x) for x in row) + "\n")

    sql_query = """
        SELECT id, date, source, format, json_extract(dataJSON, '$.sensor') as 'sensor', dataJSON
        FROM dataLogs
        WHERE id IN (
            SELECT MAX(id)
            FROM dataLogs
            WHERE source = 'sensorboard' OR source = 'sensorboard-pm'
            GROUP BY json_extract(dataJSON, '$.sensor')
        )
        ORDER BY id DESC;
    """
    results3 = run_sql_query(sql_query)
    with open(f"{filename}.txt", "a") as f:
        f.write("\nID,Date,Source,Format,Sensor,DataJSON\n")
        for row in results3:
            f.write(",".join(str(x) for x in row) + "\n")


def get_sms_message():
    base_station_id = config.ID
    zigbee_sql_query = """
    SELECT json_extract(dataJSON, '$.topic') as 'topic'
    FROM dataLogs
    WHERE source = 'zigbee' AND date >= datetime('now', '-1 day')
    GROUP BY json_extract(dataJSON, '$.topic');
    """
    zigbee_results = run_sql_query(zigbee_sql_query)
    zigbee_topics = " ".join([x[0][:2] for x in zigbee_results])

    sensorboard_sql_query = """
    SELECT json_extract(dataJSON, '$.sensor') as 'sensor'
    FROM dataLogs
    WHERE (source = 'sensorboard-pm' or source = 'sensorboard' ) AND date >= datetime('now', '-1 day') and json_extract(dataJSON, '$.sensor') != 'null'
    GROUP BY json_extract(dataJSON, '$.sensor');
    """
    sensorboard_results = run_sql_query(sensorboard_sql_query)
    sensorboard_topics = " ".join([x[0] for x in sensorboard_results])

    # print("sensorboard_topics", sensorboard_topics)
    # print("zigbee_topics", zigbee_topics)

    record_number_sql_query = """
    select MIN(id) as 'from_id' , MAX(id) as 'to_id' from dataLogs where date >= datetime('now', '-1 day')
    """
    record_number_results = run_sql_query(record_number_sql_query)
    from_id = record_number_results[0][0]
    to_id = record_number_results[0][1]
    battery_sql_query = """
    SELECT MIN(json_extract(dataJSON, '$.battery')) as 'min', MAX(json_extract(dataJSON, '$.battery')) as 'max'
    FROM dataLogs
    WHERE source = 'zigbee' AND date >= datetime('now', '-1 day');
    """
    battery_results = run_sql_query(battery_sql_query)
    battery_min = battery_results[0][0]
    battery_max = battery_results[0][1]

    temperature_sql_query = """
    SELECT MIN(json_extract(dataJSON, '$.temperature')) as 'min', MAX(json_extract(dataJSON, '$.temperature')) as 'max'
    FROM dataLogs
    WHERE source = 'zigbee' AND date >= datetime('now', '-1 day');
    """
    temperature_results = run_sql_query(temperature_sql_query)
    temperature_min = temperature_results[0][0]
    temperature_max = temperature_results[0][1]
    res = f"data=B:{base_station_id};A:{sensorboard_topics};Z:{zigbee_topics};R:{from_id},{to_id};BC:{battery_min},{battery_max};BT:{temperature_min},{temperature_max};"
    print(res)
    return res


# get_sms_message()


# get_last_datalog_by_source("last_datalogs")

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
