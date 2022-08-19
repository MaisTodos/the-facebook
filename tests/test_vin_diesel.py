import face_recognition
import numpy as np

# https://github.com/ageitgey/face_recognition/blob/master/examples/face_distance.py

NORMAL_CUTOFF = 0.6
STRICT_CUTOFF = 0.5


def test_is_vin_diesel_dominic_toretto(
    known_vin_diesel_face, known_dominic_toretto_face
):
    vin_diesel_face = np.array(known_vin_diesel_face)
    dominic_toretto_face = np.array(known_dominic_toretto_face)

    known_encodings = [vin_diesel_face]
    face_distances = face_recognition.face_distance(
        known_encodings, dominic_toretto_face
    )

    assert len(face_distances) == 1
    assert face_distances[0] < NORMAL_CUTOFF
    assert face_distances[0] < STRICT_CUTOFF
