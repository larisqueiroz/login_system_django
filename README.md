# login_system_django
<img src="assets/home.png" width="700" height= "350" title="homepage">
A login system in Python using Django.

## Description
This is a real time chat app system which allows the user to sign up, sign in using username and password (or with Google) and gives the possibility to delete the account. Also sends an email with a confirmation link when the user signs up.

## Built with
* Python (3.10.1)
* Django
* HTTP
* Ajax

## Get started
1. Install the required libs
```
pip install -r requirements.txt
```
2. Create a new Gmail account.

This project sends emails through Gmail and to do so, the code needs permition. You can do it by editing security settings on your Gmail account. However, it's not cool doing it on your personal account. So, the best choice is to create a new one for this purpose.

Turn this option ON: https://myaccount.google.com/lesssecureapps

3. Insert your email's credentials on chat_system/chat_system/info.py.

4. Run run.bat or run using an IDE with the command:
```
python chat_system/manage.py runserver
```
5. Access http://localhost:8000/

## Screenshots
<img src="assets/home.png" width="700" height= "350" title="homepage">
<img src="assets/sign up.png" width="700" height= "350" title="signup page">
<img src="assets/sign in.png" width="700" height= "350" title="signin page">
<img src="assets/google_redirect.png" width="700" height= "350" title="redirect google login">
<img src="assets/google_login.png" width="700" height= "350" title="google_login">
<img src="assets/delete.png" width="700" height= "350" title="delete">

## Contact me
LinkedIn: https://www.linkedin.com/in/larissalimaqueiroz/