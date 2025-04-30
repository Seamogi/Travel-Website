# Follow these steps to run the application

Pre-requisites: Download Python (https://www.python.org/downloads/) and make sure that Python is added to your system's PATH environment variables during installation. Download Node.js (https://nodejs.org/en/download).

1. Open the terminal and navigate to the Travel-Website-main folder path. (May need to do this twice as extracting a zip file can create a nested folder inside with the same exact name)
 
2. Run the command "pip install -r pipreqs.txt" to install all pip dependencies.

3. Create a .env file in the Travel-Website-main folder. In the .env file, create sender_gmail and email_password as empty string variables. Put your gmail address into the sender_gmail variable. Put your gmail password into the email_password variable if there is no 2 step authentication on the account. If 2 step authentication is enabled, go to this link (https://support.google.com/mail/answer/185833?hl=en) and follow the instructions to create and retrieve your app password. Once you have your app password, put it into the email_password variable in the .env file. 

4. Run the command "npm install" to install all dependencies.

5. Open another terminal and navigate to the backend folder path. Run the command "python backendapi.py" to launch the flask server. If Python is not in your system's PATH environment variables, run the command "py backendapi.py" to launch the flask server.

6. Go back to the original terminal that points to the Travel-Website-main folder path. Run the command "node server.js" to launch the server.

7. Go to http://localhost:8080 to view the website.
