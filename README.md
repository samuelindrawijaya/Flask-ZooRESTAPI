# Flask-ZooRESTAPI
This project is a RESTful API built using Flask to manage a zoo. It allows zookeepers to efficiently handle various operations related to animals and employees, including managing animal details, employee schedules, and more

## Technologies Used
- **Flask** - Python web framework for building the API.
- **PostgreSQL** - Database to store animal and employee data (via Supabase).
- **Flask SQLAlchemy** - ORM for database interactions.
- **JWT** - For secure authentication and authorization.
- **Docker** - Containerization of the application.
- **Google Cloud Run** - Cloud platform used for deployment.

## Getting Started

### Prerequisites
- **Python 3.12.5** installed
- **Docker** installed
- **Supabase PostgreSQL** database for storage
- **Postman** or similar API testing tool for testing endpoints

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/samuelindrawijaya/Flask-ZooRESTAPI

2. Install Requirement:

   ```bash
   pip install -r requirements.txt

   ```

3. Create .env:

   ```bash
    SUPABASE_DB_URL=your-supabase-postgresql-url
    JWT_SECRET_KEY=your-jwt-secret-key

   ```

4. Run db migration:

   ```bash
   flask db upgrade
   ```

5. Start the Flask application::

   ```bash
   flask run

   ```

#### The application will run at http://localhost:5000.

## Usage

- Start the development server: `flask run `


# DEPLOYMENT LINK
> [!IMPORTANT]
> This is my deployment link.
https://mute-leontyne-projectsans-7be3b426.koyeb.app/apidocs/#