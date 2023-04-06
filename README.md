# Live-Attendence-Monitoring-System
##The project will not work without a service key, follow the instructions below to generate your own as i cant provide mine as it is confidential
##here are the steps:

Go to the Firebase Console and select the project that you want to work with.
Click on the gear icon in the top left corner of the screen and select "Project settings" from the dropdown menu.
In the "Project settings" screen, go to the "Service accounts" tab.
Click on the "Generate new private key" button to generate a new service account key.
Save the key to a safe location on your computer.
Add the file path to your service account key as an environment variable in your local development environment or deployment environment.
To copy the links of the Realtime Database and Storage on Firebase:

Go to the Firebase Console and select the project that you want to work with.
For the Realtime Database, click on the "Realtime Database" tab on the left sidebar and copy the URL at the top of the page.
For the Storage, click on the "Storage" tab on the left sidebar and copy the URL at the top of the page.
In your code, you can then replace the URL placeholders with the URLs that you copied:

arduino
Copy code
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://<PROJECT_ID>.firebaseio.com/",
    'storageBucket': "<BUCKET_NAME>.appspot.com"
})
Replace <PROJECT_ID> with the ID of your Firebase project and <BUCKET_NAME> with the name of your Firebase Storage bucket.
