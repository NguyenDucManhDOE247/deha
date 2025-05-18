# Social Media Platform

A Django-based social media platform with modern features including user authentication, profiles, posts, likes, follows, and content exploration.

## 📋 Features

- **User Authentication**
  - Secure signup/login system
  - Custom validation for usernames and passwords
  - Session management

- **Profile Management**
  - Customizable user profiles
  - Profile pictures
  - Bio and location information
  - Follow/unfollow functionality

- **Content Creation**
  - Image-based posts with captions
  - Like/unlike functionality
  - Post deletion (for owned content)

- **Content Discovery**
  - Home feed with posts from followed users
  - Explore page for discovering new content
  - User and post search functionality

- **Responsive Design**
  - Bootstrap-based UI
  - Mobile-friendly layout

## 🛠️ Technologies

- **Backend**
  - Django 5.2
  - Python 3.x
  - SQLite (development)

- **Frontend**
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap 5
  - Font Awesome

- **File Storage**
  - Django's media handling for user uploads

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/socialmedia.git
   cd socialmedia
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install django pillow python-dotenv
   ```

5. **Create environment variables**
   ```bash
   # Copy the example file
   copy .env.example .env
   
   # Or create manually
   echo SECRET_KEY=django-insecure-your-secret-key-here > .env
   echo DEBUG=True >> .env
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations userauth
   python manage.py migrate
   ```

7. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Web interface: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 📁 Project Structure

```
socialmedia/
│
├── socialmedia/          # Project configuration
│   ├── settings.py       # Project settings
│   ├── urls.py           # Project URL configuration
│   ├── wsgi.py           # WSGI configuration
│   └── asgi.py           # ASGI configuration
│
├── userauth/             # Main application
│   ├── migrations/       # Database migrations
│   ├── models.py         # Data models
│   ├── views.py          # View logic
│   ├── forms.py          # Form handling
│   ├── urls.py           # URL routing
│   └── admin.py          # Admin interface configuration
│
├── templates/            # HTML templates
│   ├── main.html         # Home page
│   ├── profile.html      # User profile page
│   ├── explore.html      # Explore page
│   ├── login.html        # Login page
│   └── signup.html       # Registration page
│
├── static/               # Static files
│   ├── css/              # CSS styles
│   └── js/               # JavaScript files
│
├── media/                # User-uploaded content
│   ├── profile_images/   # Profile pictures
│   └── post_images/      # Post images
│
├── manage.py             # Django management script
├── .env                  # Environment variables
└── .env.example          # Example environment variables
```

## 👨‍💻 Development

### Adding New Features

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test thoroughly

3. Submit a pull request with a clear description of your changes

### Coding Standards

- Follow PEP 8 for Python code
- Use descriptive variable and function names
- Include docstrings for functions and classes
- Write unit tests for new functionality

## 🔒 Security

- Passwords are hashed using Django's authentication system
- CSRF protection enabled
- Form validation for user inputs
- Environment variables for sensitive settings

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- All contributors who have helped shape this project

---

Developed with ❤️ 