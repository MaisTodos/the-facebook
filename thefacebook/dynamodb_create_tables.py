from chalicelib.models import UserFaces


def dynamodb_create_tables():
    if not UserFaces.exists():
        UserFaces.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


def dynamodb_delete_tables():
    if not UserFaces.exists():
        UserFaces.delete_table()


if __name__ == "__main__":
    dynamodb_create_tables()
