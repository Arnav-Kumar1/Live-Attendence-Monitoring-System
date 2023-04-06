# Project Title

Live Attendance Tracker

## Project Description

This project uses facial recognition technology to track attendance in real-time. It captures the face of the students ( elon musk and amber heard🤣) and matches it with the stored images of students to mark their attendance in real time in firebase database.

## Technologies Used

- Python
- OpenCV
- Face Recognition Library
- Firebase Realtime Database
- Firebase Cloud Storage

## Getting Started

### Prerequisites

- Python 3.6 or higher
- OpenCV
- Face Recognition Library
- Firebase Admin SDK

### Installation

1. Clone the repo
2. Install the required libraries
3. Create a Firebase project and generate a service account key download it and store it in the same folder as the entire project (more about this step is given below in details)
4. Copy the link to your Firebase Realtime Database and Firebase Storage into the code. ( more about this step is given below in details)

### Usage

1. Add images of students  to the `images` folder
2. Once you have added the images of all the students to the image folder (there are currently only 2 images), you should include their current data into the `adddataToDatabase.py` Python file. Afterwards, execute the same file `adddataToDatabase.py` to insert the data for all the students into your firebase realtime database.
2. Run the script `Encodegenerator.py` to generate encodings of the images
3. Run the script `Attendancetracker.py` to start tracking attendance





## Installation - Step 3:
1. Go to the Firebase Console and select the project you want to work with or create a new one.
2. Click on the gear icon in the top left corner and select "Project settings" from the dropdown menu.
3. In the "Project settings" screen, go to the "Service accounts" tab.
4. Click on the "Generate new private key" button to generate a new service account key.
5. Save the key to a safe location on your computer.
6. Add the file path to your service account key as an environment variable in your local development environment or deployment environment. This step is optional
do this only if the app gives any error related to service key.


## installation step 4:

1. Go to the Firebase Console and select the project that you want to work with.
2. For the Realtime Database, click on the "Realtime Database" tab on the left sidebar and copy the URL at the top of the page.
3. For the Storage, click on the "Storage" tab on the left sidebar and copy the URL at the top of the page.
In my code, you can then replace the URL placeholders with the URLs that you copied:

these lines of code below will be found (right after import statements ) in all the 3 python files namely `app.py`, `encodegenerator.py`, `addDataTodatabse.py` :

```cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(cred,
                              {
                                  'databaseURL': "https://your-project-name-default-rtdb.firebaseio.com/",
                                  'storageBucket': "your-project-name.appspot.com"
                              })```
                              
the structure of the links which you need to copy and paste in all the 3 files in given in the above code template.
