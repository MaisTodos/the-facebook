from pynamodb.attributes import (
    UnicodeAttribute,
    ListAttribute,
)
from pynamodb.models import Model
import os


class UserFaces(Model):
    class Meta:
        table_name = "thefacebook_user_faces"
        host = os.environ.get("DYNAMODB_HOST")

    id = UnicodeAttribute(hash_key=True)
    faces = ListAttribute(null=False)
