import base64
import uuid
from io import BytesIO

import face_recognition
import numpy as np
from chalicelib.model import UserFaces
from marshmallow import EXCLUDE, Schema, ValidationError, fields, post_load, validates
from PIL import Image


class CreateUserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    image_base64 = fields.List(required=True, cls_or_instance=fields.Str)

    @validates("image_base64")
    def validate_image_base64(self, image_base64):
        self.list_of_images = []

        for image in image_base64:
            image_load = Image.open(BytesIO(base64.b64decode(image)))
            image_np = np.array(image_load)
            image_faces_detected = face_recognition.face_encodings(image_np)

            if len(image_faces_detected) != 1:
                raise ValidationError("Deve conter apenas uma pessoa na imagem.")

            self.list_of_images.append(image_faces_detected[0].tolist())

    @post_load
    def make_object(self, data, **kwargs):
        id = str(uuid.uuid4())

        user = UserFaces(id=id, faces=self.list_of_images)
        user.save()

        return id
