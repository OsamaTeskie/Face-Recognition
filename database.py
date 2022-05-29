import sqlite3
import face_recognition
import os

server = sqlite3.connect("Faces.db")
c = server.cursor()

c.execute("DROP TABLE faces")
c.execute("""CREATE TABLE faces(
    Path TEXT,
    Name TEXT
)""")

def getImages(path):
    # Get All images in the given directory and return in a list of tuples [(image encodings in bytes, file name)]
    images = []
    for filename in os.listdir(path):
        f = os.path.join(path,filename)
        if os.path.isfile(f) and (filename[-3:] == "png" or filename[-3:] == "jpg"):
            images.append((f, filename[:filename.index(".")]))
    return images


def addImagesToDB(new_images, current_images=c.execute("SELECT * FROM faces").fetchall()):
    # Loop through new_images and if an image is not in current_images then add it to the database
    for current in new_images:
        if current not in current_images:
            c.execute("INSERT INTO faces VALUES (?, ?)", (current[0], current[1]))

addImagesToDB(getImages(r"../Face_Recognition Project\images"))
server.commit()