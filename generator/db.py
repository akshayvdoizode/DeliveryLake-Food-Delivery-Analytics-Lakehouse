from sqlalchemy import create_engine
import config

def get_engine():

    connection_string = (
        f"postgresql://{config.DB_USER}:"
        f"{config.DB_PASSWORD}@"
        f"{config.DB_HOST}:"
        f"{config.DB_PORT}/"
        f"{config.DB_NAME}"
    )

    return create_engine(connection_string)

