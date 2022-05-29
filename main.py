import database
import face_recognition
import sqlite3

server = sqlite3.connect("Faces.db")
c = server.cursor()


def getFacesFromImage(image_path):
    string = 'This image has'
    
    image = face_recognition.load_image_file(image_path)
    locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, locations)
    
    answer = compareFacesFromDB(face_encodings)
    if len(answer) > 0:
        string += " {}".format(" ".join(answer))
        return string
    else:
        return "This image has no known faces"

def compareFacesFromDB(image_codes, DB_images=c.execute("SELECT * FROM faces").fetchall()):

    result = []
    for image in image_codes:
        for x in DB_images:
            current = face_recognition.load_image_file(x[0])
            code = face_recognition.face_encodings(current)[0]
            answer = face_recognition.compare_faces([image], code)
            if answer == [True]:
                result.append(x[1])
    return result

server.commit()
server.close()