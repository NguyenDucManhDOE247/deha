# Social Media Platform

A modern, Django-based social media platform with features including user authentication, profiles, posts, likes, follows, comments, tags, and content exploration.

## 📋 Features

- **User Authentication**
  - Secure signup/login system
  - Custom validation for usernames and passwords
  - Session management
  - Profile-based user accounts

- **Profile Management**
  - Customizable user profiles
  - Profile pictures and bio
  - Location information
  - Statistics for posts, followers, and following

- **Social Interaction**
  - Follow/unfollow functionality
  - Real-time follower statistics
  - Activity tracking

- **Content Creation & Management**
  - Image-based posts with captions
  - Like/unlike functionality
  - Comment system
  - Post deletion (for owned content)
  - Tag management for content organization

- **Content Organization**
  - Post tagging system
  - Tag management interface
  - Bookmark system for saving posts

- **Content Discovery**
  - Home feed with posts from followed users
  - Explore page for discovering new content
  - Tag-based content filtering
  - Advanced user and post search functionality

- **Responsive Design**
  - Bootstrap 5-based UI
  - Mobile-friendly layout
  - Intuitive user interface

## 🛠️ Technologies

- **Backend**
  - Django 5.2
  - Python 3.8+
  - SQLite (development)

- **Frontend**
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap 5
  - Font Awesome 6

- **File Storage & Media**
  - Django's media handling for user uploads
  - Image processing with Pillow

- **Development Tools**
  - Environment variable management with python-dotenv
  - Comprehensive logging system
  - Custom template tags

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

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

## 📱 Key Features & Pages

### User Management
- **Sign Up**: Create a new account with username, email, and password
- **Login**: Secure authentication system
- **Profile Management**: Update profile picture, bio, and location

### Content Interaction
- **Home Feed**: View posts from users you follow
- **Explore**: Discover new content from all users
- **Post Detail**: View individual posts with comments
- **Like/Unlike**: Interact with posts
- **Comments**: Add and delete comments on posts
- **Bookmark**: Save posts for later viewing

### Content Organization
- **Tags**: Categorize posts with custom tags
- **Tag Management**: Create, view, and delete tags
- **Tag Filtering**: View posts by specific tags

### User Interaction
- **Follow/Unfollow**: Connect with other users
- **Search**: Find users or posts by keywords
- **User Profiles**: View other users' content and stats

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
│   ├── models.py         # Data models (Profile, Post, Comment, etc.)
│   ├── views.py          # View logic
│   ├── forms.py          # Form handling (SignUp, Login, Post, etc.)
│   ├── urls.py           # URL routing
│   ├── admin.py          # Admin interface configuration
│   ├── templatetags/     # Custom template tags
│   └── context_processors.py # Global context processors
│
├── templates/            # HTML templates
│   ├── base.html         # Base template with common elements
│   ├── main.html         # Home page
│   ├── profile.html      # User profile page
│   ├── explore.html      # Explore page
│   ├── login.html        # Login page
│   ├── signup.html       # Registration page
│   ├── bookmarks.html    # Bookmarked posts page
│   ├── tag_posts.html    # Posts filtered by tag
│   ├── search_user.html  # Search results page
│   ├── comments.html     # Comments component
│   ├── modal.html        # Post creation modal
│   └── messages.html     # Flash messages component
│
├── static/               # Static files
│   ├── css/              # CSS styles
│   ├── js/               # JavaScript files
│   └── ico/              # Favicon and icons
│
├── media/                # User-uploaded content
│   ├── profile_images/   # Profile pictures
│   └── post_images/      # Post images
│
├── manage.py             # Django management script
├── .env                  # Environment variables
├── .env.example          # Example environment variables
└── README.md             # Project documentation
```

## 🔄 Database Models

- **Profile**: User profile information
- **Post**: User-created content with images and captions
- **Comment**: Comments on posts
- **LikePost**: Track post likes
- **Followers**: Track user follow relationships
- **Tag**: Post categorization
- **Bookmark**: Saved posts

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

## 🔒 Security Features

- Passwords are hashed using Django's authentication system
- CSRF protection enabled
- Form validation with custom validators
- Environment variables for sensitive settings
- Session management
- Secure permission checks for content manipulation

## ⚙️ Configuration

The project uses environment variables for configuration:

- `SECRET_KEY`: Django's secret key for cryptographic signing
- `DEBUG`: Toggle debug mode (True/False)

In production, additional security settings are automatically enabled:
- Session and CSRF cookie security
- SSL/HTTPS enforcement
- HTTP Strict Transport Security

## 🚀 Deployment Considerations

For production deployment:

1. Set `DEBUG=False` in your environment
2. Configure a production database (PostgreSQL recommended)
3. Set up proper static file serving
4. Use a WSGI server like Gunicorn or uWSGI
5. Configure a reverse proxy like Nginx
6. Set up proper media file storage (AWS S3, etc.)

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
- [Pillow](https://python-pillow.org/)
- All contributors who have helped shape this project

---

Developed with ❤️ by X