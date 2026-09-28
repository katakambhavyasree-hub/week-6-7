# Week 6,7 – Working Attendance Log 

## Overview

As part of Week 6 of my internship, I worked on developing a face recognition-based attendance system using Python. The system uses a webcam to recognize registered individuals and automatically record their attendance.

This week, I focused on implementing attendance logging, handling different edge cases, and preventing duplicate attendance entries. 
The system stores attendance details in a CSV file and maintains a log file to track its activities and errors.

## Objectives

* Automate attendance marking using face recognition.
* Recognize registered individuals by comparing facial encodings.
* Prevent duplicate attendance entries for the same person on the same day.
* Store attendance records with name, date, time, and status.
* Handle unknown faces, webcam errors, and invalid images.

## Technologies Used

* Python
* OpenCV
* Dlib
* face_recognition
* CSV and Logging modules

## Implementation

The system loads registered face images from the `known_faces` folder and generates facial encodings using the face_recognition library. When the webcam captures a face, its encoding is compared with the stored encodings to identify the person.

If a match is found, the system checks whether attendance has already been marked for that person on the current date. If not, the person's name, date, time, and status are added to `attendance.csv`. 
If attendance has already been recorded, the system prevents another entry.

Unknown individuals are displayed as "Unknown" and are not added to the attendance records.

## Logging and Edge Case Handling

Logging is implemented using Python's logging module to keep track of attendance activities, duplicate attempts, unknown face detections, and errors.

The system also handles situations such as unavailable webcams, missing or invalid face images, and frames in which no face is detected. Multiple detected faces are processed individually.

These features help make the system more reliable and easier to test and maintain.

## Project Structure

```text
week_6/
├── week6.py
├── known_faces/
│   ├── person1.jpg
│   └── person2.jpg
├── attendance.csv
└── logs/
    └── attendance.log
```

## Outcome

Successfully implemented a face recognition-based attendance system with automatic attendance recording, duplicate prevention, and error logging. This week helped me gain practical experience in face recognition,
file handling, logging, and managing real-time application errors.

## Skills Acquired

Face Recognition, Facial Encoding, OpenCV, Dlib, Python, CSV File Handling, Logging, Error Handling, and Attendance Automation.
