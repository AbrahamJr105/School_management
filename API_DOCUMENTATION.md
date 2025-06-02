# API Documentation - School Management System

## Overview
This document provides detailed information about the Django views, models, and functionality available in the School Management System.

## Models

### Student (Etudiant)
- **Fields**: nom, prenom, email, date_naissance, nationalite, sport, filiere, image
- **Relationships**: ForeignKey to Nationalite, Sport, and Filiere
- **Purpose**: Stores student information including personal details and academic program

### Teacher (Enseignant)
- **Fields**: nom, prenom, email, specialite, image
- **Purpose**: Stores teacher information and their specialties

### Grade (Note)
- **Fields**: etudiant, module, note
- **Relationships**: ForeignKey to Etudiant and Module
- **Purpose**: Stores student grades for different modules

### Module
- **Fields**: nom, enseignant
- **Relationships**: ForeignKey to Enseignant
- **Purpose**: Represents academic courses/subjects

### Academic Program (Filiere)
- **Fields**: nom
- **Purpose**: Represents different academic programs/majors

### Nationality (Nationalite)
- **Fields**: nom
- **Purpose**: Student nationality options

### Sport
- **Fields**: nom
- **Purpose**: Sports activities available to students

## Views and Endpoints

### Main Menu (`/`)
- **View**: `menu`
- **Template**: `menu.html`
- **Purpose**: Landing page with navigation to all features

### Student Management (`/etudiant/`)
- **View**: `etudiant_form`
- **Methods**: GET, POST
- **Purpose**: Add new students to the system
- **Features**: 
  - Form validation
  - Image upload support
  - Dynamic dropdowns for nationality, sport, and academic program

### Teacher Management (`/enseignant/`)
- **View**: `enseignant_form`
- **Methods**: GET, POST
- **Purpose**: Add new teachers to the system
- **Features**:
  - Form validation
  - Image upload support
  - Specialty selection

### Student Bulletin (`/bulletin/`)
- **View**: `bulletin_view`
- **Methods**: GET, POST
- **Purpose**: Generate and email student grade reports
- **Features**:
  - Student selection dropdown
  - PDF generation
  - Email functionality
  - Grade calculation (average, rank)

### Statistics (`/statistique/`)
- **View**: `statistique`
- **Purpose**: Display academic statistics and charts
- **Features**:
  - Student count by academic program
  - Average grades by module
  - Interactive charts using Chart.js
  - Chart export functionality

### PV Generation (`/pv`)
- **View**: `pv`
- **Purpose**: Generate academic committee meeting minutes (Procès-Verbal)
- **Features**:
  - Academic program selection
  - Student listing with grades
  - PDF export capability

### Authentication
- **Register** (`/register/`): User registration
- **Login** (`/login/`): User authentication
- **Logout** (`/logout/`): User logout

### Utility Endpoints
- **Chart Image Save** (`/save-chart-image/`): Save chart images for reports

## Database Schema

### Relationships
```
Etudiant ──┬── Nationalite (ForeignKey)
           ├── Sport (ForeignKey)
           └── Filiere (ForeignKey)

Note ──┬── Etudiant (ForeignKey)
       └── Module (ForeignKey)

Module ── Enseignant (ForeignKey)
```

## Features

### 1. Student Management
- Complete CRUD operations
- Image upload and management
- Association with academic programs, nationalities, and sports

### 2. Teacher Management
- Teacher registration with specialties
- Image upload support

### 3. Grade Management
- Grade entry and tracking
- Association with students and modules
- Grade statistics and analysis

### 4. Reporting System
- Student bulletins with PDF generation
- Email delivery of reports
- Academic statistics with visual charts

### 5. Academic Administration
- PV (meeting minutes) generation
- Program-based student listings
- Grade analysis and ranking

## Technical Stack

### Backend
- **Django 5.1.3**: Web framework
- **SQLite**: Database (configurable for PostgreSQL)
- **Python**: Core programming language

### Frontend
- **HTML5/CSS3**: Modern web standards
- **Bootstrap**: Responsive UI framework
- **Chart.js**: Interactive charts and graphs
- **JavaScript**: Dynamic functionality

### Additional Libraries
- **Pillow**: Image processing
- **ReportLab**: PDF generation
- **Django Debug Toolbar**: Development debugging

## Security Features
- User authentication system
- Form validation and sanitization
- CSRF protection
- Media file security

## Performance Considerations
- Optimized database queries
- Image compression and resizing
- Efficient template rendering
- Static file optimization

## Error Handling
- Comprehensive form validation
- User-friendly error messages
- Graceful degradation for missing data
- Logging system for debugging

## Future Enhancements
- API endpoints for mobile applications
- Advanced reporting features
- Real-time notifications
- Integration with external systems
- Multi-language support
