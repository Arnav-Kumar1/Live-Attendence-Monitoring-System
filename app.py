import os
import pickle
import cv2
import cvzone
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials, db, storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
                              {
                                  'databaseURL': "https://live-attendance-tracker-default-rtdb.firebaseio.com/",
                                  'storageBucket': "live-attendance-tracker.appspot.com"
                              })

bucket = storage.bucket()

cap = cv2.VideoCapture(0)  # The cv2.VideoCapture() function is commonly used to create an object ( here cap) that can
# be used to capture frames from a video stream ( in a while loop) or a video file.cap stands for capture
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')  # cv2.imread() function reads an image in the BGR color format
# by default,The function  is used to read an image file from disk and load it into a NumPy array, which can then
# be used for further image processing tasks. The output this fun is a NumPy array representing the loaded image.

mode_folder_path = 'Resources/Modes'
modepathList = os.listdir(mode_folder_path)  # this var stores names of files inside the given location in a list
# print(modepathList)


imgModeList = []
for path in modepathList:
    imgModeList.append(cv2.imread(os.path.join(mode_folder_path, path)))

print("reading encoded file")

# load the encoded file
file = open("encodedfile.p", 'rb')  # rb is read binary
encodings_list_with_corresponding_IDS = pickle.load(file)  # encodings on images of musk and amber
file.close()
print("finished loading encoded file")

encodings_list, student_ids = encodings_list_with_corresponding_IDS

mode_type = 0  # inside the mode folder there are 4 images, each one of this 4 are represented
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()  # The function cap.read() reads the next frame from the video stream cap and returns
    # two values: a boolean success indicating whether the frame was successfully read or not, and the actual frame
    # images data represented in numpy array where each element represent a pixel in the image which has a greyscale
    # value between  0 to 255

    img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # resizes the captured frame from webcam footage to a
    # smaller size by a factor of 0.25
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)  # change the color format to RGB, because RGB is used by
    # face recognition library where as open cv captures webcam frames in BGR format

    imgBackground[162:162 + 480, 55:55 + 640] = img  # superimposing the background image over the output of webcam
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[mode_type]  # superimposing one of the image at 0 index
    # over the output of webcam

    # cv2.imshow("WebCam", img)  # name of the window is webcam, uncomment to show the raw webcam output without any
    # superimposed images

    location_of_faces_inTheFootage = face_recognition.face_locations(img_small)
    # The face_locations() function can be used to detect the locations of one or more faces in an image
    encode_faces_inTheFootage = face_recognition.face_encodings(img_small, location_of_faces_inTheFootage)
    # The face_encodings() function takes these parameters and returns a list of 128-dimensional numeric vectors

    for current_encoded_faceInWebcam, current_face_loc in zip(encode_faces_inTheFootage,
                                                              location_of_faces_inTheFootage):
        matches = face_recognition.compare_faces(encodings_list,
                                                 current_encoded_faceInWebcam)  # matches :  [False, False, False]
        # compare_faces returns a list of n elements where n boolean elements where n corresponds to number of
        # images in the encoding_list, True says that the nth image is matched against the instantaneous frame
        # in the webcam footage
        face_distance = face_recognition.face_distance(encodings_list, current_encoded_faceInWebcam)  # lower the
        # face distance better the match

        match_index = np.argmin(face_distance)  # arg_min returns the index of the minimum value in the given list
        # the minimum value in the face-distance list will always be the one corresponding to matched face, hence
        # match_index carries the index of the matched face, now we can use this index value to extract the ID of
        # the matched face from the student id list

        if matches[match_index]:  # matches[match_index] will correspond to TRUE when the face is detected
            # print("face Detected", "student ID :", student_ids[match_index])
            y1, x2, y2, x1 = current_face_loc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # scale dimensions back , up by factor of 4

            bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)  # setting a box around the face as soon
            # as its detected

            id = student_ids[match_index]  # id for whatever face was detected

            if counter == 0:
                counter = 1  # set the counter to 1 as soon as the face is detected
                mode_type = 1

    if counter != 0:

        if counter == 1:  # the first frame of the detected face

            student_info = db.reference("Students/{}".format(id)).get()
            print(student_info)

            # get the image from the storage
            blob = bucket.get_blob(f'images/{id}.png')  # get the photo of the detected face
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

        cv2.putText(imgBackground, str(student_info['total attendance']), (861, 125),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 1)

        cv2.putText(imgBackground, str(student_info['major']), (1006, 550),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (255, 255, 255), 1)

        cv2.putText(imgBackground, str(id), (1006, 493),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (255, 255, 255), 1)

        cv2.putText(imgBackground, str(student_info['GPA']), (910, 625),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, (100, 100, 100), 1)

        cv2.putText(imgBackground, str(student_info['year']), (1025, 625),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, (100, 100, 100), 1)

        cv2.putText(imgBackground, str(student_info['starting year']), (1125, 625),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (100, 100, 100), 1)

        (width, height), _ = cv2.getTextSize(student_info['name'], cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 1)
        offset = (414 - width) // 2  # width of the mode 1 image upon which we superimpose all these values is 414
        cv2.putText(imgBackground, str(student_info['name']), (808 + offset, 445),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (50, 50, 50), 1)

        # imgStudent_resized = cv2.resize(imgStudent, (216, 216))
        imgBackground[175:175+216, 909:909+216] = imgStudent

        counter += 1

    cv2.imshow("Face Attendence", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit the window
        break

cap.release()
cv2.destroyAllWindows()
