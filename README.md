# 🌐 Django Social Media App

A full-stack social media application built with Django. Users can register, create posts, upload images, like/dislike content, follow other users, and edit their profiles. Designed with clean UI and secure authentication.

---

## 🚀 Features

- 🔐 User registration and login/logout
- 📝 Create, edit, and delete posts
- 📷 Upload and view images
- 👍 Like / 👎 Dislike posts
- 🧑 User profiles with bio and profile picture
- 🔎 Explore public posts


---

## 🛠️ Tech Stack

- **Backend:** Django
- **Database:** PostgreSQL
- **Authentication:** Django built-in
- **Media:** Django cloudinary

## 🧩 Models Overview

### `User` (Custom)
```python
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', default='default.jpg')


🧑‍💻 Getting Started
1. Clone the repository
bash
git clone https://github.com/yourusername/social_media.git
cd social_media

2. Create virtual environment and install dependencies
bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

3. Set up the database
bash
python manage.py makemigrations
python manage.py migrate

4. Create a superuser (for admin access)
bash
python manage.py createsuperuser

5. Run the server
bash
Copy
Edit
python manage.py runserver


