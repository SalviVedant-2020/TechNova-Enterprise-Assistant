from pathlib import Path

from langchain_community.utilities import SQLDatabase


BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "database" / "company.db"


db = SQLDatabase.from_uri(
    f"sqlite:///{DATABASE_PATH}"
)


def get_schema():

    return db.get_table_info()


def execute_sql(query: str):

    try:

        result = db.run(query)

        return True, result

    except Exception as e:

        return False, str(e)
    
def get_table_names():

    return sorted(db.get_usable_table_names())