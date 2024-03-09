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
    db_name = params.db
    table_name = params.table
    csv_url = params.url
    csv_name = "output.csv"

    print(f"Downloading and unzipping csv data from {csv_url}")

    os.system(f"curl -L '{csv_url}' | gunzip > {csv_name}")

    print("Creating engine...")
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db_name}")

    print("Constructing dataframe...")
    chunksize = 1000000
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=chunksize)

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    print("Creating table...")
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")

    i = 0
    while True:
        print(f"Iteration {i}")
        t_start = time()

        df = next(df_iter)

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists="append")

        t_end = time()

        print(f"Inserted {chunksize} records after %.3f seconds" % (t_end - t_start))

        i += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    # user, password, host, port, db name, table name, csv url

    parser.add_argument("--user", help="pg username")
    parser.add_argument("--password", help="pg pw")
    parser.add_argument("--host", help="pg host")
    parser.add_argument("--port", help="pg port")
    parser.add_argument("--db", help="postgres db name")
    parser.add_argument("--table", help="postgres table name")
    parser.add_argument("--url", help="csv_url")

    args = parser.parse_args()

    main(args)
