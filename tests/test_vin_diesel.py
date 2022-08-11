import face_recognition

# https://github.com/ageitgey/face_recognition/blob/master/examples/face_distance.py

NORMAL_CUTOFF = 0.6
STRICT_CUTOFF = 0.5


def test_is_vin_diesel_dominic_toretto():
    vin_diesel = face_recognition.load_image_file("tests/_vin_diesel.jpg")
    vin_diesel_face = face_recognition.face_encodings(vin_diesel)[0]

    dominic_toretto = face_recognition.load_image_file("tests/_dominic_toretto.jpg")
    dominic_toretto_face = face_recognition.face_encodings(dominic_toretto)[0]

    known_encodings = [vin_diesel_face]
    face_distances = face_recognition.face_distance(
        known_encodings, dominic_toretto_face
    )

    assert len(face_distances) == 1
    assert face_distances[0] < NORMAL_CUTOFF
    assert face_distances[0] < STRICT_CUTOFF
