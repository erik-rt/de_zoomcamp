import argparse
import pandas as pd
import os
from time import time
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db

    taxi_table_name = params.taxi_table
    taxi_url = params.taxi_url

    zone_table_name = params.zone_table
    zone_url = params.zone_url

    print("Creating engine...")
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    print(f"Downloading and unzipping taxi csv data from {taxi_url}")
    csv_name = "taxi_output.csv"
    os.system(f"curl -L '{taxi_url}' | gunzip > {csv_name}")

    print(f"Constructing dataframe from {csv_name}...")
    chunksize = 100000
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=chunksize)

    df = next(df_iter)

    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    print(f"Creating table {taxi_table_name}...")
    df.head(n=0).to_sql(name=taxi_table_name, con=engine, if_exists="replace")

    i = 0
    while True:
        try:
            print(f"Iteration {i}")
            t_start = time()

            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

            df.to_sql(name=taxi_table_name, con=engine, if_exists="append")

            t_end = time()

            print(
                f"Inserted {chunksize} records after %.3f seconds" % (t_end - t_start)
            )

            df = next(df_iter)
            i += 1
        except StopIteration:
            print("Finished inserting all records")
            break

    print(f"Downloading and unzipping zone csv data from {zone_url}")
    csv_name = "zone_output.csv"

    # No need to gunzip since it's a csv file
    os.system(f"curl -o {csv_name} {zone_url}")

    print(f"Constructing dataframe from {csv_name}...")
    chunksize = 100
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=chunksize)

    df = next(df_iter)

    print(f"Creating table {zone_table_name}...")
    df.head(n=0).to_sql(name=zone_table_name, con=engine, if_exists="replace")

    i = 0
    while True:
        try:
            print(f"Iteration {i}")
            t_start = time()

            df.to_sql(name=zone_table_name, con=engine, if_exists="append")

            t_end = time()

            print(
                f"Inserted {chunksize} records after %.3f seconds" % (t_end - t_start)
            )

            df = next(df_iter)
            i += 1
        except StopIteration:
            print("Finished inserting all records")
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    # user, password, host, port, db name, table name, csv url

    parser.add_argument("--user", help="pg username")
    parser.add_argument("--password", help="pg pw")
    parser.add_argument("--host", help="pg host")
    parser.add_argument("--port", help="pg port")
    parser.add_argument("--db", help="pg db name")
    parser.add_argument("--taxi_table", help="taxi table name")
    parser.add_argument("--taxi_url", help="taxi data csv url")
    parser.add_argument("--zone_table", help="zone table name")
    parser.add_argument("--zone_url", help="zone data csv url")

    args = parser.parse_args()

    main(args)
