# Testing Guide - School Management System

## Overview
This guide provides comprehensive testing procedures to verify all functionality of the School Management System.

## Prerequisites
1. Django development server running (`python manage.py runserver`)
2. Database populated with sample data (`python manage.py populate_db`)
3. Superuser account created (`python manage.py createsuperuser`)

## Manual Testing Procedures

### 1. Main Menu Testing
**URL**: `http://127.0.0.1:8000/`

**Test Cases**:
- [ ] Page loads without errors
- [ ] Navigation links are present and functional
- [ ] Responsive design works on different screen sizes
- [ ] CSS and styling load correctly

**Expected Results**:
- Clean, modern interface
- All navigation links clickable
- No JavaScript errors in browser console

### 2. Student Management Testing
**URL**: `http://127.0.0.1:8000/etudiant/`

**Test Cases**:
- [ ] Form loads with all required fields
- [ ] Dropdown fields populate with data (nationality, sport, filiere)
- [ ] Form validation works (required fields, email format)
- [ ] Image upload functionality
- [ ] Successful form submission
- [ ] Error handling for invalid data

**Steps**:
1. Navigate to student form
2. Fill all required fields
3. Upload a valid image file
4. Submit form
5. Verify success message
6. Test with invalid data (empty required fields, invalid email)

### 3. Teacher Management Testing
**URL**: `http://127.0.0.1:8000/enseignant/`

**Test Cases**:
- [ ] Form loads correctly
- [ ] Specialty dropdown populated
- [ ] Form validation works
- [ ] Image upload functionality
- [ ] Successful submission

**Steps**:
1. Navigate to teacher form
2. Fill all fields including specialty
3. Upload teacher image
4. Submit and verify success

### 4. Statistics Page Testing
**URL**: `http://127.0.0.1:8000/statistique/`

**Test Cases**:
- [ ] Page loads without template errors
- [ ] Charts render correctly using Chart.js
- [ ] Data displays accurately
- [ ] Chart interactions work (hover, click)
- [ ] Export functionality works

**Steps**:
1. Navigate to statistics page
2. Verify charts display data
3. Test chart interactions
4. Check for JavaScript errors
5. Test chart export feature

### 5. Bulletin Generation Testing
**URL**: `http://127.0.0.1:8000/bulletin/`

**Test Cases**:
- [ ] Student dropdown populated with existing students
- [ ] Grade data displays correctly for selected student
- [ ] PDF generation works
- [ ] Email functionality works (if configured)
- [ ] Error handling for students without grades

**Steps**:
1. Navigate to bulletin page
2. Select a student from dropdown
3. Verify grade information displays
4. Test PDF generation
5. Test email sending (if email configured)

### 6. PV Generation Testing
**URL**: `http://127.0.0.1:8000/pv`

**Test Cases**:
- [ ] Page loads without template errors
- [ ] Academic program dropdown populated
- [ ] Student data displays correctly for selected program
- [ ] Grade information accurate
- [ ] PDF export functionality

**Steps**:
1. Navigate to PV page
2. Select an academic program
3. Verify student listing with grades
4. Test PDF generation functionality

### 7. Admin Interface Testing
**URL**: `http://127.0.0.1:8000/admin/`

**Test Cases**:
- [ ] Admin login works with superuser credentials
- [ ] All models visible in admin
- [ ] CRUD operations work for all models
- [ ] Field configurations correct (especially Note model)
- [ ] No field name errors

**Steps**:
1. Login with superuser account
2. Test each model (Etudiant, Enseignant, Note, Module, etc.)
3. Create, read, update, delete records
4. Verify field configurations work correctly

### 8. Authentication Testing

**Register** (`/register/`):
- [ ] Registration form works
- [ ] Validation prevents duplicate users
- [ ] Password requirements enforced

**Login** (`/login/`):
- [ ] Valid credentials allow login
- [ ] Invalid credentials rejected
- [ ] Redirects work correctly

**Logout** (`/logout/`):
- [ ] User successfully logged out
- [ ] Session cleared properly

## Database Testing

### Data Integrity Tests
- [ ] Foreign key relationships work correctly
- [ ] Cascade deletes function properly
- [ ] Data validation at model level

### Sample Data Verification
- [ ] 5 nationalities created
- [ ] 6 sports available
- [ ] 4 academic programs (filieres)
- [ ] 3 teachers with modules
- [ ] 4 students enrolled
- [ ] 8 grade records

### Commands Testing
```bash
# Test management commands
python manage.py populate_db  # Should complete without errors
python manage.py migrate      # Should show "No migrations to apply"
python manage.py collectstatic # Should collect static files
```

## Performance Testing

### Load Testing
- [ ] Page load times under 3 seconds
- [ ] Database queries optimized
- [ ] Image uploads process efficiently
- [ ] No memory leaks during extended use

### Stress Testing
- [ ] Multiple concurrent users
- [ ] Large file uploads
- [ ] Bulk data operations

## Error Handling Testing

### Expected Errors
- [ ] 404 for non-existent URLs
- [ ] Form validation errors display properly
- [ ] File upload errors handled gracefully
- [ ] Database connection errors

### Browser Compatibility
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari (if available)
- [ ] Edge

## Security Testing

### Input Validation
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] CSRF token validation
- [ ] File upload security

### Authentication
- [ ] Access control works
- [ ] Session management secure
- [ ] Password handling proper

## Automated Testing

### Running Django Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test myapp

# Run with verbosity
python manage.py test --verbosity=2
```

### Test Coverage
- Models: Create, read, update, delete operations
- Views: GET and POST requests
- Forms: Validation and processing
- Templates: Rendering without errors

## Common Issues and Solutions

### Template Errors
- **Issue**: JavaScript/Django template conflicts
- **Solution**: Separate Django variables from JavaScript code
- **Test**: Verify no template syntax errors in browser

### Admin Field Errors
- **Issue**: Field name mismatches in admin.py
- **Solution**: Use lowercase field names matching model definitions
- **Test**: Admin interface loads without errors

### Database Issues
- **Issue**: Migration problems
- **Solution**: Reset migrations if needed, ensure model syntax correct
- **Test**: Migrations apply cleanly

### Static Files
- **Issue**: CSS/JS not loading
- **Solution**: Run `collectstatic`, check STATIC_URL settings
- **Test**: Styling appears correctly

## Deployment Testing

### Production Readiness
- [ ] DEBUG = False works correctly
- [ ] Static files serve properly
- [ ] Database connections stable
- [ ] Error pages display correctly

### Environment Variables
- [ ] Sensitive settings externalized
- [ ] Database credentials secure
- [ ] Email settings configured

## Final Verification Checklist

- [ ] All URLs accessible without errors
- [ ] Forms submit and validate correctly
- [ ] Charts and visualizations display
- [ ] PDF generation functional
- [ ] Admin interface fully operational
- [ ] Database populated with sample data
- [ ] No JavaScript console errors
- [ ] Responsive design works
- [ ] Image uploads successful
- [ ] Email functionality tested (if configured)

## Reporting Issues

When reporting issues, include:
1. URL where issue occurred
2. Steps to reproduce
3. Expected vs actual behavior
4. Browser and version
5. Error messages or screenshots
6. Server logs if available

## Performance Benchmarks

Target performance metrics:
- Page load: < 3 seconds
- Form submission: < 2 seconds
- Chart rendering: < 1 second
- PDF generation: < 5 seconds
- Database queries: < 100ms average
