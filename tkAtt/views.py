from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from userprofile.models import *

import cv2
import os
import numpy as np
import pickle,joblib
from mtcnn import MTCNN
from keras_facenet import FaceNet
from django.conf import settings

# Create your views here.
# Path to the pre-trained model file (Smodel.pkl)
# model_path = os.path.join(settings.BASE_DIR, 'tkAtt', 'models', 'Smodel.pkl')
model_path = os.path.join(settings.BASE_DIR, 'tkAtt', 'models', 'Smodelnabil.pkl')
# model_path = os.path.join(settings.BASE_DIR, "tkAtt", "models", "updatedmodel.pkl")


#nabil pkl model list
label_names = {
        3: 'Mim', 2: 'Ishfaq', 5: 'Nabil', 8: 'Raiyan', 6: 'Poran', 4: 'Minhaj', 16: 'protik', 7: 'Prapti', 
        9: 'Sakib', 10: 'Sam',
        11: 'Showrov', 17: 'samia', 13: 'Tahia', 12: 'Sinthia', 15: 'Vabna', 0: 'Fahim', 14: 'Tithi', 1: 'Ira',
    }
# label for Smodels
# label_names = {
#         0: "Fahim",
#         1: "Ishfaq",
#         2: "Mahin",
#         3: "Mim",
#         4: "Minhaj",
#         5: "Poran",
#         6: "Prapti",
#         7: "Rabby",
#         8: "Rafiur",
#         9: "Raiyan",
#         10: "sakib",
#         11: "Saam",
#         12: "Shohail",
#         13: "Showrov",
#         14: "Sinthia",
#         15: "tahia",
#         16: "tithi",
#         17: "Vabna",
#         18: "Nabil",
#         19: "Samia",
#         # Add more label-name mappings as needed
#     }
#updated pkl model list 
# label_names = {
#     14: "Sinthia",
#     12: "Shohail",
#     1: "Ishfaq",
#     13: "Showrov",
#     16: "Tithi",
#     17: "Vabna",
#     2: "Mahin",
#     3: "Mim",
#     15: "Tahia",
#     0: "Fahim",
#     4: "Minhaj",
#     19: "samia",
#     10: "Sakib",
#     8: "Rafiur",
#     9: "Raiyan",
#     5: "Poran",
#     7: "Rabby",
#     18: "nabil",
#     11: "Sam",
#     6: "Prapti",
# }
# Define the directory name and path to store face images
directory_name = "temp"
directory_path = os.path.join(settings.BASE_DIR, "tkAtt", directory_name)


# Create your views here.
@login_required(login_url="login")
def tkAtt(request, course_name, section_number):
    vid = cv2.VideoCapture(1)  # Use 0 for default webcam, or change to another number if using an external camera
    predicted_names = set()

    # Initialize MTCNN detector and FaceNet embedder
    detector = MTCNN()
    embedder = FaceNet()
    # Confidence threshold for predictions (adjust as needed)
    confidence_threshold = 0.5

    def get_embedding(face_img):
        face_img = face_img.astype("float32")  # Convert to float32
        face_img = np.expand_dims(face_img, axis=0)
        embeddings = embedder.embeddings(face_img)  # Generate embeddings
        return embeddings[0]

    #Load the trained model for face recognition
    with open(model_path, "rb") as file:
        model = pickle.load(file)
    # # joblib
    # # Load model with joblib
    # model = joblib.load(model_path)
    # Create 'temp' directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    while True:
        # Capture frame-by-frame
        success, frame = vid.read()

        if not success:
            print("Failed to capture frame from webcam")
            break

        # Detect faces in the frame
        faces = detector.detect_faces(frame)

        for i, face in enumerate(faces):
            # Get bounding box coordinates
            x, y, w, h = face["box"]

            # Extract face region from the frame
            face_img = frame[y : y + h, x : x + w]

            # Preprocess face image for prediction
            face_img = cv2.resize(face_img, (160, 160))  # Resize to FaceNet input size
            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)  # Convert to RGB

            # Save each detected face as an image in 'temp' directory
            face_image_path = os.path.join(directory_path, f"face_{x}_{y}_{w}_{h}.jpg")
            cv2.imwrite(
                face_image_path, cv2.cvtColor(face_img, cv2.COLOR_RGB2BGR)
            )  # Save face image

            # Compute embedding for the detected face
            embedding = get_embedding(face_img)
            embedding = np.expand_dims(embedding, axis=0)  # Reshape for prediction

            # Use the loaded model to predict the person for the current face
            prediction = model.predict(embedding)
            ypreds_proba = model.predict_proba(embedding)
            print("Predicted Probabilities:", ypreds_proba)
            # Get the index of the class with the highest probability
            predicted_class_index = np.argmax(ypreds_proba)

            # Get the highest probability value
            prob = ypreds_proba[0, predicted_class_index]

            # Define your threshold (e.g., 0.5 or any value suitable for your use case)
            threshold = 0.60
            # Assuming 'ypreds_proba' is a list of probabilities for the first (and only) sample
            if prob <= threshold:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    "unknown",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 0, 255),
                    2,
                )
            else:
                predicted_label = prediction[0]
                predicted_name = label_names.get(predicted_label, "Unknown")
                print("Predicted Person:", predicted_name)
                # results=check(predicted_name,course_name, section_number)
                predicted_names.add(predicted_name)
                # Display predicted name under the face on the frame
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    predicted_name,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2,
                )

        # Display the frame with detected faces and predicted names
        cv2.imshow("output", frame)

        # Check for 'q' key pressed to exit loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release video capture object and close all windows
    vid.release()
    cv2.destroyAllWindows()
    # Remove images from the temporary folder after the loop
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        os.remove(file_path)

    # After closing the windows, call the check function with the collected predicted names
    results = []
    for predicted_name in predicted_names:
        result = check(predicted_name, course_name, section_number)
        results.append(result)
    print(results)
    context = {
        "results": results,
    }
    return render(request, "tkAtt.html", context)

    # return redirect('check', data1=list(predicted_names), data2=course_name ,data3=section_number)


from django.db import transaction
from datetime import date


@transaction.atomic
def check(student_name, course_name, section_number):
    assignments = []
    try:
        # Get the course object
        course = Course.objects.get(name=course_name, section_number=section_number)

        # Check if the student is assigned to the course
        is_assigned = Student.objects.filter(name=student_name, courses=course).exists()

        # # Check if attendance record exists for the student in the course
        # attendance_recorded = Attendance.objects.filter(student__name=student_name, course=course).exists()

        # Determine attendance status
        if is_assigned:

            # If attendance is not recorded, create a new attendance record
            Attendance.objects.create(
                student=Student.objects.get(name=student_name), course=course
            )
            attendance_status = "Recorded"

            # Append assignment status to assignments list
            assignments.append(
                {
                    "student_name": student_name,
                    "is_assigned": is_assigned,
                    "attendance": attendance_status,
                }
            )

            # Print assignment status
            print(
                f"{student_name} is assigned to {course_name} - Section {section_number}. Attendance: {attendance_status}"
            )
        else:
            assignments.append(
                {
                    "student_name": student_name,
                    "is_assigned": is_assigned,
                    "attendance": "Not Recorded",
                }
            )
            print(
                f"{student_name} is not assigned to {course_name} - Section {section_number}"
            )

        return assignments

    except Course.DoesNotExist:
        # Handle the case where the course does not exist
        print("Error: Course does not exist")
        return []
