# Social Media Platform - DEHA

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
  - Django
  - Python 3.11+
  - SQLite database

- **Frontend**
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap 5
  - Font Awesome

- **File Storage & Media**
  - Django's media handling for user uploads
  - Image processing with Pillow

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/deha.git
   cd deha
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
   pip install django pillow
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
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
deha/
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
│   ├── messages.html     # Flash messages component
│   ├── edit_profile.html # Profile editing page
│   └── manage_tags.html  # Tag management page
│
├── static/               # Static files
│   ├── css/              # CSS styles
│   ├── js/               # JavaScript files
│   └── ico/              # Favicon and icons
│
├── staticfiles/          # Collected static files for production
│
├── media/                # User-uploaded content
│   ├── profile_images/   # Profile pictures
│   └── post_images/      # Post images
│
├── manage.py             # Django management script
├── db.sqlite3            # SQLite database
├── debug.log             # Debug logs
└── README.md             # Project documentation
```

## 🔄 Database Models

The application uses the following main models:
- User profiles
- Posts
- Comments
- Likes
- Followers
- Tags
- Bookmarks

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

## 🔒 Security Features

- Passwords are hashed using Django's authentication system
- CSRF protection enabled
- Form validation with custom validators
- Session management
- Secure permission checks for content manipulation

## ⚙️ Configuration

The project uses Django's settings system for configuration:
- Debug mode can be enabled/disabled in settings.py
- Media and static file paths are configured
- Database settings can be adjusted as needed

## 🚀 Deployment

For production deployment:
1. Set `DEBUG=False` in settings.py
2. Configure a production database (PostgreSQL recommended)
3. Set up proper static file serving
4. Use a WSGI server like Gunicorn
5. Configure a reverse proxy like Nginx
6. Set up proper media file storage

## 📄 License

This project is licensed under the MIT License.

---

Developed with ❤️