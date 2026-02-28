# ASTU Digital Lost & Found System

A web-based platform for Arsi University students to report lost and found items, search, and claim belongings securely.

## Features

- User registration and authentication
- Report lost or found items with image upload
- Search and filter items by category, status, and keyword
- Submit claims on found items
- Admin approval/rejection workflow for claims
- Dashboard with statistics (admin only)
- Responsive design (mobile, tablet, desktop)
- Security measures: login required for actions, owner-only edit/delete, CSRF protection

## Tech Stack

- **Backend:** Django 4/5, SQLite (development)
- **Frontend:** Bootstrap 5, Bootstrap Icons, custom CSS
- **Other:** Django ORM, Pillow for images

## Installation

1. Clone the repository:
```bash
   git clone https://github.com/yourusername/astu-lost-found.git
   cd astu-lost-found
   ```
2. Create and activate a virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```
3. Install dependencies:

```bash
pip install django pillow
```
4. Apply migrations:

```bash
python manage.py migrate
```
5. Create a superuser (admin):

```bash
python manage.py createsuperuser
```
6. Run the development server:

```bash
python manage.py runserver
```
7. Visit http://127.0.0.1:8000 in your browser.