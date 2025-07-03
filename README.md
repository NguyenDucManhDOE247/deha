# Social Media Platform

A modern, Django-based social media platform with features including user authentication, profiles, posts, likes, follows, comments, tags, and content exploration.

## 📋 Features

- **User Authentication**
  - Secure signup/login system with custom validation
  - Username and password validation with regex patterns
  - Remember me functionality for extended sessions
  - Profile-based user accounts

- **Profile Management**
  - Customizable user profiles with bio and location
  - Profile picture uploads and management
  - Real-time profile statistics (posts, followers, following)
  - Edit profile functionality with form validation

- **Social Interaction**
  - Follow/unfollow functionality with real-time updates
  - Follower/following statistics
  - User search functionality with pagination

- **Content Creation & Management**
  - Image-based posts with captions
  - Multiple tag selection for posts
  - Like/unlike functionality with real-time counters
  - Comment system with AJAX support
  - Post deletion with permission checks
  - Tag management for content organization

- **Content Organization**
  - Post tagging system with multi-select capability
  - Tag management interface (create, view, delete)
  - Bookmark system for saving favorite posts

- **Content Discovery**
  - Home feed showing posts from followed users
  - Personalized content filtering
  - Explore page for discovering content from all users
  - Tag-based content filtering
  - Advanced user and post search functionality

- **Responsive Design**
  - Bootstrap 5-based UI
  - Mobile-friendly layout
  - Intuitive navigation and user interface
  - FontAwesome icons integration
  - CSS animations and transitions

## 🛠️ Technologies

- **Backend**
  - Django 5.2.1
  - Python 3.11+
  - SQLite database
  - Class-based views architecture

- **Frontend**
  - HTML5 with Django templates
  - CSS3 with custom styling and animations
  - JavaScript for interactive features
  - Bootstrap 5 for responsive design
  - Font Awesome icons
  - AJAX for asynchronous operations

- **File Storage & Media**
  - Django's media handling for user uploads
  - Image processing with Pillow
  - Structured media directories for organization

- **Security**
  - Django's built-in security features
  - Custom password validators
  - CSRF protection
  - Secure session management
  - Permission-based access control

- **UI/UX Design**
  - Custom CSS variables system
  - Responsive grid layouts
  - Animation effects for user interactions
  - Card-based content design
  - Custom tooltips and notification indicators

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
   pip install django pillow python-dotenv
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
- **Sign Up**: Create a new account with custom validation for username and password
- **Login**: Secure authentication with remember me option
- **Profile Management**: Upload/change profile picture, edit bio and location information

### Content Interaction
- **Home Feed**: View posts from users you follow, sorted by recent activity
- **Explore**: Discover new content from all users in a grid layout
- **Post Detail**: View individual posts with comments and interaction options
- **Like/Unlike**: Interactive post liking with real-time counter updates
- **Comments**: Add and delete comments with permission checks
- **Bookmark**: Save posts for later viewing in a dedicated bookmarks page

### Content Organization
- **Tags**: Create and add multiple tags to posts
- **Tag Management**: Create, view, and delete tags from a dedicated interface
- **Tag Filtering**: View posts filtered by specific tags
- **Bookmarks Collection**: Access all saved posts in one location

### User Interaction
- **Follow/Unfollow**: Connect with other users with one click
- **Search**: Find users or posts by keywords with paginated results
- **User Profiles**: View user statistics, posts, and follow status

## 📁 Project Structure

```
deha/
│
├── socialmedia/          # Project configuration
│   ├── settings.py       # Project settings with environment variables
│   ├── urls.py           # Main URL configuration
│   ├── wsgi.py           # WSGI configuration
│   └── asgi.py           # ASGI configuration
│
├── userauth/             # Main application
│   ├── migrations/       # Database migrations
│   ├── models.py         # Data models (Profile, Post, Comment, etc.)
│   ├── views.py          # Class-based views for all functionality
│   ├── forms.py          # Form classes with validation
│   ├── urls.py           # App URL routing
│   ├── admin.py          # Admin interface customization
│   ├── templatetags/     # Custom template filters
│   └── context_processors.py # Global context processors
│
├── templates/            # HTML templates
│   ├── base.html         # Base template with common elements
│   ├── main.html         # Home feed
│   ├── profile.html      # User profile page
│   ├── explore.html      # Explore page for content discovery
│   ├── login.html        # Login page
│   ├── signup.html       # Registration page
│   ├── bookmarks.html    # Bookmarked posts page
│   ├── tag_posts.html    # Posts filtered by tag
│   ├── search_user.html  # Search results page
│   ├── comments.html     # Comments component
│   ├── modal.html        # Post creation modal
│   ├── messages.html     # Flash messages component
│   ├── edit_profile.html # Profile editing page
│   ├── manage_tags.html  # Tag management page
│   └── favicon_include.html # Favicon includes
│
├── static/               # Static files
│   ├── css/              # CSS styles with app.css
│   ├── js/               # JavaScript files
│   └── ico/              # Favicon and icon files
│
├── media/                # User-uploaded content
│   ├── profile_images/   # Profile pictures
│   ├── post_images/      # Post images
│   └── blank-profile-picture.png # Default profile image
│
├── manage.py             # Django management script
├── db.sqlite3            # SQLite database
├── debug.log             # Debug and error logs
└── README.md             # Project documentation
```

## 🔄 Database Models

The application uses the following main models:

- **Profile**: Extended user information (bio, location, profile picture)
  - Connected to Django's built-in User model
  - Stores personal information and profile image

- **Post**: User-created content
  - UUID-based primary key for secure URLs
  - Image storage with uploaded files
  - Caption text and creation timestamp
  - Like counter and tag relationships

- **Tag**: Content categorization
  - Unique name field
  - Many-to-many relationship with posts

- **Comment**: User interaction on posts
  - Text content with timestamps
  - References to parent post and author

- **LikePost**: Tracks user likes
  - Records which users liked which posts
  - Used for like/unlike toggling

- **Followers**: Tracks user connections
  - Records follower and followed user relationships
  - Enforces unique relationships

- **Bookmark**: Saved content
  - Records which users bookmarked which posts
  - Enforces unique bookmarks per user

## 💎 UI/UX Design System

DEHA uses a sophisticated design system built on CSS variables and custom components:

### Core Design Elements

- **Color Palette**
  - Primary: Black (#000000)
  - Secondary: Dark Gray (#404040)
  - Accent: Medium Gray (#707070)
  - Background: White (#FFFFFF)
  - Text: Black (#000000) and Gray (#404040)
  - Border: Light Gray (#E0E0E0)

- **Typography**
  - System font stack with fallbacks
  - Clear hierarchy with varied font weights
  - Optimized line height (1.6) for readability

- **Animation System**
  - Fade-in effects for content loading
  - Hover transitions for interactive elements
  - Transform animations for buttons and cards
  - Pulse animations for notification indicators

- **Component Design**
  - Card-based post layout with hover effects
  - Custom form elements with floating labels
  - Gradient backgrounds for visual hierarchy
  - Consistent border radiuses and shadow styles

### Responsive Design

- Fluid layouts that adapt to different screen sizes
- Mobile-first approach with media queries
- Sidebar collapses to horizontal navigation on small screens
- Responsive image handling to maintain performance

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
- Use Django's class-based views where appropriate
- Follow CSS naming conventions for styling

## 🔒 Security Features

- Passwords are hashed using Django's authentication system
- CSRF protection enabled for all forms
- Form validation with custom regex validators
- Session management with remember me functionality
- Login-required decorators and mixins
- Permission checks for content manipulation
- Secure media file handling
- Protection against SQL injection via ORM

## ⚙️ Configuration

The project uses Django's settings system with environment variables:
- Environment variables loaded via python-dotenv
- Debug mode togglable via environment settings
- Media and static file paths configured
- Database settings adjustable
- Comprehensive logging configuration
- Session expiry settings

## 🧪 Testing

To run the test suite:

```bash
python manage.py test
```

Key testing areas:
- Authentication workflows
- Post creation and interaction
- User following functionality
- Tag and bookmark systems
- Form validations

## 🌐 Browser Support

The application is designed to work on modern browsers:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Android Chrome)

## 🚀 Deployment

For production deployment:
1. Set `DEBUG=False` in environment variables
2. Configure a production database (PostgreSQL recommended)
3. Set up proper static file serving
4. Use a WSGI server like Gunicorn
5. Configure a reverse proxy like Nginx
6. Set up proper media file storage
7. Enable HTTPS with properly configured settings
8. Implement media file optimization and caching

## 📄 License

This project is licensed under the MIT License.

---

Developed with ❤️ by Nguyen Duc Manh
