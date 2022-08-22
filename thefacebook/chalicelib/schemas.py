import base64
import uuid
from io import BytesIO

import face_recognition
import numpy as np
from chalicelib.models import UserFaces
from marshmallow import (
    EXCLUDE,
    Schema,
    ValidationError,
    fields,
    post_load,
    pre_load,
    validates,
)
from PIL import Image
from pynamodb.exceptions import DoesNotExist


class CreateUserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    images_base64 = fields.List(required=True, cls_or_instance=fields.Str)

    @validates("images_base64")
    def validate_images_base64(self, images_base64):
        self.list_of_images = []

        for image in images_base64:
            image_load = Image.open(BytesIO(base64.b64decode(image)))
            image_rgb = image_load.convert("RGB")
            image_np = np.array(image_rgb)
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


class ValidateUserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    image_base64 = fields.Str(required=True)
    user_id = fields.UUID(required=True)
    cutoff = fields.Float(required=False, missing=0.5)

    @pre_load
    def validate_user_exist(self, data, **kwargs):
        try:
            self.user = UserFaces.get(str(data["user_id"]))

        except DoesNotExist:
            raise ValidationError("Usuário não encontrado.", "user_id")

        except KeyError:
            pass

        return data

    @validates("image_base64")
    def validate_image_base64(self, image_base64):
        image_load = Image.open(BytesIO(base64.b64decode(image_base64)))
        image_rgb = image_load.convert("RGB")
        image_np = np.array(image_rgb)
        images_face_detected = face_recognition.face_encodings(image_np)

        if len(images_face_detected) != 1:
            raise ValidationError("Deve conter apenas uma pessoa na imagem.")

        self.new_face = images_face_detected[0]

    @post_load
    def make_object(self, data, **kwargs):
        known_faces = [np.array(face) for face in self.user.faces]
        face_distances = face_recognition.face_distance(
            face_encodings=known_faces, face_to_compare=self.new_face
        )
        is_valid = all(distance < data["cutoff"] for distance in face_distances)

        if is_valid:
            self.user.faces.append(self.new_face.tolist())
            self.user.save()

        payload = {
            "is_valid": is_valid,
            "cutoff": data["cutoff"],
            "distances": face_distances.tolist(),
        }
        return payload
