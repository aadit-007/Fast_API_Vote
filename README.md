# FastAPI Backend Project

A robust and scalable FastAPI-based backend application with user authentication, post management, and voting system.

## 🚀 Features

- **User Authentication**
  - JWT token-based authentication
  - Secure password hashing with bcrypt
  - OAuth2 with password flow

- **Post Management**
  - Create, read, update, and delete posts
  - Filter and sort posts
  - Pagination support

- **Voting System**
  - Upvote/downvote posts
  - Prevent duplicate votes
  - Track vote counts

- **Database**
  - PostgreSQL database support
  - SQLAlchemy ORM
  - Alembic database migrations

- **API Documentation**
  - Interactive API documentation at `/docs`
  - Automatic request/response validation
  - Example requests and responses

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT, OAuth2
- **API Documentation**: Swagger UI, ReDoc
- **Migrations**: Alembic
- **Environment Management**: python-dotenv

## 📦 Prerequisites

- Python 3.9+
- PostgreSQL
- pip (Python package manager)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Fast_API-Backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory with the following variables:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/dbname
   SECRET_KEY=your-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Access the API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📚 API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token

### Users
- `GET /users/me` - Get current user details
- `GET /users/{id}` - Get user by ID
- `POST /users/` - Create a new user (admin only)

### Posts
- `GET /posts/` - Get all posts (with pagination)
- `GET /posts/{id}` - Get a specific post
- `POST /posts/` - Create a new post (authenticated)
- `PUT /posts/{id}` - Update a post (owner only)
- `DELETE /posts/{id}` - Delete a post (owner/admin)

### Votes
- `POST /votes/` - Vote on a post
- `GET /votes/{post_id}` - Get vote count for a post

## 🔧 Configuration

Update the following environment variables in your `.env` file as needed:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secret key for JWT token generation
- `ALGORITHM`: Hashing algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30 minutes)

## 🌟 Future Enhancements

### High Priority
- [ ] Add email verification for new user registration
- [ ] Implement password reset functionality
- [ ] Add rate limiting to prevent abuse
- [ ] Implement refresh tokens for better security

### Medium Priority
- [ ] Add user roles and permissions
- [ ] Implement file uploads (for post images)
- [ ] Add full-text search for posts
- [ ] Implement user following/followers system

### Low Priority
- [ ] Add push notifications
- [ ] Implement WebSocket for real-time updates
- [ ] Add social login (Google, GitHub, etc.)
- [ ] Implement API versioning

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the amazing framework
- SQLAlchemy for the ORM
- All contributors who helped improve this project
