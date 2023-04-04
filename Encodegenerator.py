import cv2
import os
import pickle
import face_recognition

import firebase_admin
from firebase_admin import storage, credentials

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://live-attendance-tracker-default-rtdb.firebaseio.com/",
    'storageBucket': "live-attendance-tracker.appspot.com"})

# importing student images

folder_path = 'images'
pathList = os.listdir(folder_path)  # this var stores names of files inside the given location in a list
# print(pathList) # ['65895.png', '99866.jpg']
# print(pathList)
imgList = []

student_ids = []  # ['65895', '99866']
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folder_path, path)))

    student_ids.append(os.path.splitext(path)[0])  # ['65895', '99866']
    # os.path.splitext(path)  # output : ('65895', '.png'),('99866', '.jpg') this splits the filename and now we can
    # only select the first part of the filename which is the part without file extension, the reason we do this and not
    # the slicing is because the numbers can change or increase or decrease in length at that time slicing will give
    # error
    filename = "{}/{}".format(folder_path, path)
    bucket = storage.bucket()  # creates a new Bucket object, which represents a bucket in Google Cloud Storage.
    # This object is used to perform various operations on the bucket, such as uploading and downloading files
    blob = bucket.blob(filename)  # blob = bucket.blob(filename) creates a new Blob object,
    # which represents a file in the bucket. The filename argument specifies the name of the file that will be uploaded
    # to the bucket
    blob.upload_from_filename(filename)  # uploads the file to the bucket


def findEncoding(list_of_images):
    encode_list = []
    for img in list_of_images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # convert the BGR read image to RGB as face_recognition lib uses
        # RGB color scheme
        encode = face_recognition.face_encodings(img)[0]
        # The face_encodings() function returns a list of face encodings for all the faces detected in the input image.
        # The [0] index selects the first face encoding in the list, while [1] selects the second face encoding,
        # and so on. It's worth noting that the number of face encodings in the list returned by face_encodings()
        # will depend on the number of faces detected in the input image.

        encode_list.append(encode)
    return encode_list


print("encoding started...")
encodings_list = findEncoding(imgList)
print("encoding ended")

encodings_list_with_corresponding_IDS = [encodings_list, student_ids]

file = open("encodedfile.p", 'wb')
# opens a file named "encodedfile.p" in binary write mode. The wb mode specifies that the file is opened for writing
# in binary mode. If the file does not exist, it will be created. If it already exists, its contents will be
# overwritten.When a file is opened in binary write mode ('wb'), it means that the data being written to the
# file is in binary format, rather than text format
pickle.dump(encodings_list_with_corresponding_IDS, file)
file.close()
