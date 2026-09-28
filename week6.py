import cv2
import face_recognition
import os
import csv
import logging
from datetime import datetime


KNOWN_FACES_FOLDER = "week_6/known_faces"
ATTENDANCE_FILE = "week_6/attendance.csv"
LOG_FOLDER = "week_6/logs"
LOG_FILE = os.path.join(LOG_FOLDER, "attendance.log")



os.makedirs(LOG_FOLDER, exist_ok=True)



logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


if not os.path.exists(ATTENDANCE_FILE):

    with open(ATTENDANCE_FILE, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Name",
            "Date",
            "Time",
            "Status"
        ])


known_face_encodings = []
known_face_names = []

print("Loading known faces...")

for filename in os.listdir(KNOWN_FACES_FOLDER):

    if filename.lower().endswith(
        (".jpg", ".jpeg", ".png")
    ):

        image_path = os.path.join(
            KNOWN_FACES_FOLDER,
            filename
        )

        try:

            image = face_recognition.load_image_file(
                image_path
            )

            encodings = face_recognition.face_encodings(
                image
            )

            if len(encodings) == 0:

                print(
                    f"No face found in {filename}"
                )

                logging.warning(
                    f"No face found in {filename}"
                )

                continue

            encoding = encodings[0]

            known_face_encodings.append(
                encoding
            )

            name = os.path.splitext(filename)[0]

            known_face_names.append(name)

            print(
                f"Loaded: {name}"
            )

            logging.info(
                f"Known face loaded: {name}"
            )

        except Exception as error:

            print(
                f"Error loading {filename}: {error}"
            )

            logging.error(
                f"Error loading {filename}: {error}"
            )


print()
print("Known people:", known_face_names)

def already_marked(name):

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    try:

        with open(
            ATTENDANCE_FILE,
            "r",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                if (
                    row["Name"] == name
                    and row["Date"] == today
                ):

                    return True

        return False

    except Exception as error:

        logging.error(
            f"Attendance check error: {error}"
        )

        return False

def mark_attendance(name):

    if already_marked(name):

        print(
            f"{name} - Already marked today"
        )

        logging.info(
            f"Duplicate attendance prevented: {name}"
        )

        return False


    now = datetime.now()

    date = now.strftime(
        "%Y-%m-%d"
    )

    time = now.strftime(
        "%H:%M:%S"
    )


    try:

        with open(
            ATTENDANCE_FILE,
            "a",
            newline=""
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                name,
                date,
                time,
                "Present"
            ])


        print(
            f"Attendance marked: {name}"
        )

        logging.info(
            f"Attendance marked: {name}"
        )

        return True


    except Exception as error:

        print(
            f"Could not save attendance: {error}"
        )

        logging.error(
            f"Could not save attendance: {error}"
        )

        return False


camera = cv2.VideoCapture(0)


if not camera.isOpened():

    print("ERROR: Could not access webcam")

    logging.error(
        "Could not access webcam"
    )

    exit()


print()
print("==============================")
print("FACE ATTENDANCE SYSTEM")
print("==============================")
print("Press Q to exit")
print()


logging.info(
    "Attendance system started"
)


while True:

    ret, frame = camera.read()


    if not ret:

        print(
            "Could not read webcam frame"
        )

        logging.error(
            "Could not read webcam frame"
        )

        break


    # =========================
    # RESIZE FRAME
    # =========================

    small_frame = cv2.resize(
        frame,
        (0, 0),
        fx=0.25,
        fy=0.25
    )


    rgb_small_frame = cv2.cvtColor(
        small_frame,
        cv2.COLOR_BGR2RGB
    )


    face_locations = face_recognition.face_locations(
        rgb_small_frame
    )


    face_encodings = face_recognition.face_encodings(
        rgb_small_frame,
        face_locations
    )


    for face_encoding, face_location in zip(
        face_encodings,
        face_locations
    ):

        matches = face_recognition.compare_faces(
            known_face_encodings,
            face_encoding,
            tolerance=0.5
        )


        name = "Unknown"

        if len(known_face_encodings) > 0:

            face_distances = face_recognition.face_distance(
                known_face_encodings,
                face_encoding
            )

            best_match_index = face_distances.argmin()


            if matches[best_match_index]:

                name = known_face_names[
                    best_match_index
                ]


        top, right, bottom, left = face_location

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4


        if name == "Unknown":

            logging.warning(
                "Unknown person detected"
            )

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                (0, 0, 255),
                2
            )

            cv2.putText(
                frame,
                "Unknown",
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

            continue


        marked = mark_attendance(name)


        if marked:

            display_text = (
                f"{name} - Present"
            )

        else:

            display_text = (
                f"{name} - Already Marked"
            )


        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            display_text,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )



    cv2.imshow(
        "Face Attendance System",
        frame
    )




    if cv2.waitKey(1) & 0xFF == ord("q"):

        logging.info(
            "Attendance system stopped"
        )

        break


camera.release()

cv2.destroyAllWindows()

print()
print("Attendance system stopped.")