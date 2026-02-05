# Packadive Backend

Backend API for packadive - a checklist management application for dive trip planning.

## Description

Packadive Backend is a Flask-based REST API that provides user authentication, checklist management, and list item tracking functionality. Built with SQLAlchemy for database operations and includes features like rate limiting, caching, and API documentation support.

## Features

- **User Management**: User registration, authentication, and profile management
- **Checklist Management**: Create, read, update, and delete checklists
- **List Items**: Manage individual items within checklists with status tracking
- **Rate Limiting**: API rate limiting to prevent abuse
- **Caching**: Response caching for improved performance
- **Database**: PostgreSQL support with SQLAlchemy ORM
- **Security**: Password hashing with Werkzeug
- **API Documentation**: Swagger/OpenAPI support (configurable)

## Technology Stack

- **Framework**: Flask 3.1.2
- **Database ORM**: SQLAlchemy 2.0.44 with Flask-SQLAlchemy 3.1.1
- **Serialization**: Marshmallow 4.1.0 with flask-marshmallow 1.3.0
- **Database**: PostgreSQL (psycopg2-binary 2.9.11)
- **Authentication**: python-jose 3.5.0 for JWT tokens
- **Rate Limiting**: Flask-Limiter 4.0.0
- **Caching**: Flask-Caching 2.3.1
- **Server**: Gunicorn 23.0.0

## Database Schema

### User

- `id`: Primary key
- `user_name`: Unique username (max 50 chars)
- `password`: Hashed password (max 100 chars)
- `email`: Unique email address (max 100 chars)
- Relationships: One-to-many with CheckList

### CheckList

- `id`: Primary key
- `checklist_name`: Name of the checklist (max 100 chars)
- `user_id`: Foreign key to User
- Relationships: Many-to-one with User, One-to-many with ListItems

### ListItems

- `id`: Primary key
- `item_name`: Name of the item (max 100 chars)
- `status`: Status of the item (max 20 chars)
- `checklist_id`: Foreign key to CheckList
- Relationships: Many-to-one with CheckList

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL database

### Setup

1. Clone the repository:

```bash
git clone https://github.com/Joefb/packadive-backend.git
cd packadive-backend
```

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Configure environment variables (create a `.env` file or set them in your environment):

```bash
export FLASK_APP=planadive.py
export FLASK_ENV=development  # or production
export DATABASE_URL=postgresql://username:password@localhost/dbname
```

1. Initialize the database:

```bash
flask db upgrade  # If using Flask-Migrate
# Or the database will be initialized on first run
```

## Running the Application

### Development Mode

```bash
python planadive.py
```

The application will create a default admin user on first run:

- **Username**: `admin`
- **Password**: `password`
- **Email**: `admin@admin.com`

⚠️ **Security Warning**: Change the admin password immediately after first run!

### Production Mode

```bash
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app('production')"
```

## API Endpoints

### User Endpoints (`/user`)

- User registration, login, and profile management

### Checklist Endpoints (`/checklists`)

- Create, read, update, and delete checklists
- List all checklists for a user

### List Item Endpoints (`/list_item`)

- Manage items within checklists
- Update item status

## Configuration

The application uses configuration classes defined in `config.py`. Available configurations:

- Development
- Production
- Testing (if configured)

## Project Structure

```
packadive-backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── extensions.py        # Flask extensions initialization
│   ├── blueprints/          # API route blueprints
│   │   ├── user.py
│   │   ├── checklist.py
│   │   └── list_item.py
│   ├── util/                # Utility functions
│   └── static/              # Static files (Swagger specs, etc.)
├── instance/                # Instance-specific files (database, etc.)
├── config.py                # Configuration settings
├── planadive.py             # Application entry point
├── requirements.txt         # Python dependencies
└── README.md
```

## Development

### Adding New Features

1. Create new models in `app/models.py`
2. Create new blueprints in `app/blueprints/`
3. Register blueprints in `app/__init__.py`
4. Update configuration in `config.py` as needed

### Database Migrations

If using Flask-Migrate:

```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

## Security Considerations

- Change the default admin password immediately
- Use environment variables for sensitive configuration
- Enable HTTPS in production
- Configure rate limiting appropriately for your use case
- Use strong secret keys for JWT tokens
- Regularly update dependencies

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see below for details.

MIT License

Copyright (c) 2026 Joefb

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contact

Project Owner: [Joefb](https://github.com/Joefb)

Project Link: [https://github.com/Joefb/packadive-backend](https://github.com/Joefb/packadive-backend)
