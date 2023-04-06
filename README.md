# Live-Attendence-Monitoring-System
## The project will not work without a service key, follow the instructions below to generate your own as i cant provide mine as it is confidential
## here are the steps:

1.Go to the Firebase Console and select the project or make a new one that you want to work with.
2.Click on the gear icon in the top left corner of the screen and select "Project settings" from the dropdown menu.
3.In the "Project settings" screen, go to the "Service accounts" tab.
4.Click on the "Generate new private key" button to generate a new service account key.
5.Save the key to a safe location on your computer.
6.Add the file path to your service account key as an environment variable in your local development environment or deployment environment.

##  To copy your links ( as my links wont work as soon as the service key is changed obviously) of the Realtime Database and Storage on Firebase:

1.Go to the Firebase Console and select the project that you want to work with.
2.For the Realtime Database, click on the "Realtime Database" tab on the left sidebar and copy the URL at the top of the page.
3.For the Storage, click on the "Storage" tab on the left sidebar and copy the URL at the top of the page.
In my code, you can then replace the URL placeholders with the URLs that you copied:

these lines of code below wil be found (right after import statements ) in all the 3 python files namely app.py, encodegenerator.py, addDataTodatabse.py :

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,
                              {
                                  'databaseURL': "https://your-project-name-default-rtdb.firebaseio.com/",
                                  'storageBucket': "your-project-name.appspot.com"
                              })
the structure of the links which you need to copy and paste in all the 3 files in given in the above code template.
