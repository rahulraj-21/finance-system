\# Finance Tracker API



A Python-based finance tracking system built with FastAPI, SQLAlchemy, and SQLite.



\## Tech Stack

\- FastAPI

\- SQLite + SQLAlchemy

\- Pydantic

\- JWT Authentication (python-jose)

\- Passlib + bcrypt for password hashing



\## Setup Instructions



1\. Clone the repository

2\. Create a virtual environment:

&#x20;  python -m venv venv

&#x20;  venv\\Scripts\\activate



3\. Install dependencies:

&#x20;  pip install -r requirements.txt

&#x20;  pip install bcrypt==4.0.1



4\. Seed the database with test data:

&#x20;  python seed.py



5\. Run the server:

&#x20;  uvicorn app.main:app --reload



6\. Open API docs:

&#x20;  http://127.0.0.1:8000/docs



\## Test Credentials

| Role    | Email                  | Password    |

|---------|------------------------|-------------|

| Admin   | admin@finance.com      | admin123    |

| Analyst | analyst@finance.com    | analyst123  |

| Viewer  | viewer@finance.com     | viewer123   |



\## API Endpoints



\### Auth

\- POST /auth/register - Register a new user

\- POST /auth/login - Login and get JWT token

\- GET /auth/me - Get current logged in user



\### Transactions

\- GET /transactions/ - List all transactions (with filters)

\- POST /transactions/ - Create a transaction

\- GET /transactions/{id} - Get a single transaction

\- PUT /transactions/{id} - Update a transaction

\- DELETE /transactions/{id} - Delete a transaction



\### Analytics

\- GET /analytics/summary - Total income, expenses, balance

\- GET /analytics/categories - Spending by category

\- GET /analytics/monthly - Monthly breakdown

\- GET /analytics/recent - Last 5 transactions



\### Admin

\- GET /admin/users - List all users

\- DELETE /admin/users/{id} - Delete a user

\- PUT /admin/users/{id}/role - Change user role

\- GET /admin/transactions - View all transactions



\## Roles

\- Viewer: Can view transactions and summary

\- Analyst: Can view, filter, and access detailed analytics

\- Admin: Full access including user management



\## Assumptions

\- Each user can only see their own transactions

\- Viewers cannot create, update, or delete transactions

\- Admin role is assigned manually or at registration

\- Dates follow YYYY-MM-DD format

\- Transaction type is either "income" or "expense"



\## Project Structure

finance\_system/

├── app/

│   ├── main.py        # App entry point and auth routes

│   ├── models.py      # SQLAlchemy database models

│   ├── schemas.py     # Pydantic request/response schemas

│   ├── database.py    # Database connection

│   ├── auth.py        # JWT auth and role logic

│   └── routers/

│       ├── transactions.py

│       ├── analytics.py

│       └── admin.py

├── seed.py            # Test data

└── README.md

