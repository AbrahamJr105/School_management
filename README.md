# 🎓 Django School Management System

A comprehensive web-based school management system built with Django, featuring modern UI/UX design and robust functionality for managing students, teachers, grades, and academic operations.

![Django](https://img.shields.io/badge/Django-5.1.3-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

## 📋 Table of Contents

- [Features](#-features)
- [Models Overview](#-models-overview)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Technologies Used](#-technologies-used)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 👥 User Management
- **Authentication System**: Secure login/logout with role-based access (Staff/Student)
- **User Roles**: Differentiated access levels for administrators and students
- **Registration**: New user registration with role assignment

### 👨‍🎓 Student Management
- **Student Profiles**: Comprehensive student information management
- **Personal Details**: Name, address, nationality, date of birth
- **Academic Information**: Field of study (Filière), enrollment details
- **Extracurricular**: Sports activities and platform preferences
- **Image Upload**: Student photo management
- **CRUD Operations**: Create, Read, Update, Delete student records

### 👨‍🏫 Teacher Management
- **Teacher Profiles**: Complete teacher information system
- **Professional Details**: Academic grade, specialty, contact information
- **Academic Hierarchy**: Support for various academic ranks (Assistant to Professor)
- **Specializations**: Multiple subject specialties (Computer Science, Mathematics, etc.)
- **CRUD Operations**: Full teacher record management

### 📚 Academic Management
- **Module System**: Course/subject management with coefficients
- **Grade Management**: Student grade recording and calculation
- **Weighted Averages**: Automatic calculation based on module coefficients
- **Academic Programs**: Filière (field of study) management
- **Pass/Fail Status**: Automatic determination based on grade thresholds

### 📊 Statistics & Analytics
- **Dashboard**: Modern statistical overview with interactive charts
- **Student Statistics**: Gender distribution, enrollment numbers
- **Grade Analytics**: Performance metrics and trends
- **Visual Charts**: Chart.js integration for data visualization
- **Responsive Design**: Mobile-friendly statistical displays

### 📄 Transcript Generation (PV)
- **Grade Transcripts**: Official academic transcript generation
- **Program-based Reports**: Filter by academic program
- **Email Integration**: Send transcripts via email
- **Print Support**: Print-friendly transcript layouts
- **Chart Integration**: Visual grade distribution charts
- **Export Options**: Multiple output formats

### 📧 Communication
- **Email System**: Integrated email functionality for transcripts
- **HTML Templates**: Professional email templates
- **Chart Attachments**: Send visual charts via email
- **Bulk Operations**: Multiple recipient support

### 🎯 Modern UI/UX
- **Responsive Design**: Mobile-first approach
- **Modern Styling**: CSS Grid, Flexbox, and modern CSS features
- **Interactive Elements**: Hover effects, transitions, and animations
- **Color-coded Status**: Visual indicators for pass/fail status
- **Professional Templates**: Clean, modern template design
- **Form Validation**: Client-side and server-side validation

## 📱 Screenshots

### Dashboard
![Dashboard Preview](docs/dashboard-preview.png)
*Modern dashboard with statistics cards and interactive charts*

### Student Management
![Student Form](docs/student-form-preview.png)
*Comprehensive student information form with modern UI*

### Grade Transcripts
![Transcript View](docs/transcript-preview.png)
*Professional transcript generation with charts and email integration*

## 🗃️ Models Overview

### Core Models

#### 🎓 **Etudiant (Student)**
- Personal information (name, address, nationality)
- Academic details (program, enrollment)
- Extracurricular activities (sports)
- Contact information and preferences
- Image upload support

#### 👨‍🏫 **Enseignant (Teacher)**
- Professional information (grade, specialty)
- Personal details (contact, address)
- Academic qualifications
- Teaching assignments

#### 📚 **Module**
- Course/subject information
- Credit coefficients for grading
- Teaching assignments
- Program associations

#### 📝 **Note (Grade)**
- Student-module grade relationships
- Weighted grade calculations
- Pass/fail determinations
- Date tracking

#### 🏫 **Filiere (Academic Program)**
- Fields of study management
- Program descriptions
- Student-program associations

#### 🌍 **Nationalite (Nationality)**
- Country code management
- Nationality information

#### ⚽ **Sport**
- Sports activities catalog
- Student-sport relationships

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/school-management-system.git
cd school-management-system
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration
Create a `.env` file in the project root:
```env
# Database Configuration
DB_NAME=school_management
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
EHU=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Django Settings
SECRET_KEY=your_secret_key_here
DEBUG=True
```

### Step 5: Database Setup
```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Step 6: Collect Static Files
```bash
python manage.py collectstatic
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## ⚙️ Configuration

### Database Configuration
The project supports multiple database backends:

#### PostgreSQL (Recommended for Production)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

#### SQLite (Development)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Email Configuration
Configure SMTP settings in `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EHU')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')
```

### Media Files
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## 💻 Usage

### User Roles

#### 🔐 **Staff/Admin Users**
- Full access to all features
- Student and teacher management
- Grade management and statistics
- Transcript generation and email

#### 👨‍🎓 **Student Users**
- Limited access to bulletin/transcript viewing
- Personal information access

### Core Workflows

#### 1. Student Registration
1. Navigate to Student Management
2. Click "Add New Student"
3. Fill in personal and academic information
4. Upload student photo (optional)
5. Save the record

#### 2. Grade Management
1. Access Django Admin panel
2. Navigate to Notes (Grades)
3. Add grades for student-module combinations
4. System automatically calculates weighted averages

#### 3. Transcript Generation
1. Go to PV (Transcript) section
2. Select academic program (Filière)
3. View generated transcript with statistics
4. Email or print the transcript

#### 4. Statistics Dashboard
1. Access Statistics section
2. View interactive charts and metrics
3. Analyze student distribution and performance

### Navigation

#### Main Menu Options:
- **Etudiant**: Student management interface
- **Enseignant**: Teacher management interface
- **Tableaux**: Django admin panel access
- **Bulletin**: Individual student transcripts
- **Statistique**: Statistics dashboard
- **PV**: Program transcripts and reports

## 🔗 API Endpoints

| Endpoint | Method | Description | Access Level |
|----------|--------|-------------|--------------|
| `/` | GET | Main menu/dashboard | Staff |
| `/login/` | GET, POST | User authentication | Public |
| `/register/` | GET, POST | User registration | Public |
| `/logout/` | POST | User logout | Authenticated |
| `/etudiant/` | GET, POST | Student management | Staff |
| `/enseignant/` | GET, POST | Teacher management | Staff |
| `/bulletin/` | GET, POST | Student bulletins | All Users |
| `/statistique/` | GET | Statistics dashboard | Staff |
| `/pv/` | GET, POST | Program transcripts | Staff |
| `/save-chart-image/` | POST | Chart image saving | Staff |
| `/admin/` | GET | Django admin panel | Superuser |

## 📁 Project Structure

```
School_management/
├── 📁 myproject/              # Django project configuration
│   ├── __init__.py
│   ├── settings.py           # Project settings
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── 📁 myapp/                 # Main application
│   ├── 📁 migrations/        # Database migrations
│   ├── 📁 templates/         # HTML templates
│   │   ├── 📁 accounts/      # Authentication templates
│   │   └── 📁 myapp/         # Application templates
│   │       ├── base.html     # Base template
│   │       ├── menu.html     # Navigation menu
│   │       ├── etudiant_form.html    # Student form
│   │       ├── enseignant_form.html  # Teacher form
│   │       ├── statistique.html      # Statistics dashboard
│   │       ├── pv.html              # Transcript generation
│   │       ├── bulletin.html        # Student bulletin
│   │       └── html_content.html    # Email template
│   ├── 📁 static/            # Static files (CSS, JS, images)
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Django forms
│   ├── admin.py             # Admin interface
│   └── urls.py              # App URL patterns
├── 📁 media/                 # User uploaded files
├── requirements.txt         # Python dependencies
├── Pipfile                  # Pipenv configuration
├── manage.py               # Django management script
├── .env                    # Environment variables
└── README.md               # This file
```

## 🛠️ Technologies Used

### Backend
- **Django 5.1.3**: Web framework
- **Python 3.8+**: Programming language
- **PostgreSQL**: Database (production)
- **SQLite**: Database (development)

### Frontend
- **HTML5**: Markup language
- **CSS3**: Styling with modern features (Grid, Flexbox)
- **JavaScript**: Client-side functionality
- **Chart.js**: Interactive charts and graphs

### Libraries & Tools
- **Pillow**: Image processing
- **python-dotenv**: Environment variable management
- **django-debug-toolbar**: Development debugging
- **WeasyPrint**: PDF generation
- **gunicorn**: WSGI HTTP Server
- **whitenoise**: Static file serving

### Development Tools
- **Git**: Version control
- **pip**: Package management
- **Pipenv**: Virtual environment management

## 🚀 Deployment

### Production Setup

#### 1. Environment Variables
```env
DEBUG=False
SECRET_KEY=your_production_secret_key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

#### 2. Static Files
```bash
python manage.py collectstatic --noinput
```

#### 3. Database Migration
```bash
python manage.py migrate
```

#### 4. Gunicorn Configuration
```bash
gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
```

### Heroku Deployment
1. Create `Procfile`:
```
web: gunicorn myproject.wsgi
```

2. Configure environment variables in Heroku dashboard
3. Deploy using Heroku CLI or GitHub integration

## 📚 Documentation

This project includes comprehensive documentation to help developers and administrators:

### 📖 Available Documentation
- **[Configuration Guide](CONFIGURATION.md)** - Detailed setup and configuration instructions
- **[API Documentation](API_DOCUMENTATION.md)** - Complete API reference with models, views, and endpoints
- **[Testing Guide](TESTING_GUIDE.md)** - Comprehensive testing procedures and test cases
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Production deployment instructions for various environments

### 🔧 Quick Documentation Links
- **Installation**: See [CONFIGURATION.md](CONFIGURATION.md) for detailed setup
- **API Reference**: Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for all endpoints
- **Testing**: Follow [TESTING_GUIDE.md](TESTING_GUIDE.md) for comprehensive testing
- **Deployment**: Use [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for production setup

### 📋 Documentation Features
- Step-by-step installation guides
- Complete API endpoint documentation
- Database schema and relationships
- Security best practices
- Performance optimization tips
- Troubleshooting guides
- Testing procedures and checklists

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Workflow
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Code Standards
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Write unit tests for new features
- Update documentation as needed

### Testing
```bash
# Run tests
python manage.py test

# Check code coverage
coverage run --source='.' manage.py test
coverage report
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django community for the excellent framework
- Chart.js for interactive charting capabilities
- Contributors and testers who helped improve this project

---