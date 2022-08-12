from chalicelib.model import UserFaces


def dynamodb_create_tables():
    if not UserFaces.exists():
        UserFaces.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)


if __name__ == "__main__":
    dynamodb_create_tables()
