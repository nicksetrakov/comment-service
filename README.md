# Comment System

Comment System is an application for managing comments with the ability to add, delete, and reply to comments. The project uses Django for the backend and PostgreSQL for data storage. Redis and RabbitMQ are configured for asynchronous tasks, channels and caching.

## Features

- **Create and Manage Comments**: Users can create comments and manage them. Comments can be edited or deleted by their authors or administrators.
- **Media Files**: Attach images and text files to comments. Image files are resized to ensure they do not exceed a certain dimension.
- **Replies to Comments**: Comments can have replies, which are displayed as nested comments, allowing for threaded discussions.
- **Sorting**: Comments can be sorted by user, email, and creation date, providing flexible views of the comment data.
- **Security**: Implemented access controls ensure that only authenticated users can create comments and users can edit or delete comments only own comments. Permissions are managed through custom Django permissions.
- **Celery Integration**: Utilizes Celery for handling asynchronous tasks, such as processing background tasks with send email to user parent comment.
- **Web Socket Integration**: Real-time updates and notifications for new comments and replies through WebSocket channels, enhancing user interaction.
- **Swagger Integration**: Comprehensive API documentation available through Swagger, providing interactive API exploration and testing.
- **Caches by Redis**: Implements caching using Redis to improve performance and reduce database load for frequently accessed data.
- **Django Signals Integration**: Utilizes Django signals to trigger events or actions based on certain events within the application, such as creating comments.


## Installation and Running with Docker

### Requirements

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.



1. **Clone the repository:**

   ```sh
   git clone https://github.com/nicksetrakov/comment-service
   cd comment-service
   ```
   
2. Create an `.env` file in the root of the project directory. You can use the `.env.sample` file as a template:

   ```sh
   cp .env.example .env
   ```
3. Create app images and start it:
   ```sh
   docker-compose build
   docker-compose up
   ```
and try to open http://127.0.0.1:8001/api/doc/swagger

### You can login with these credentials:
```
username: admin
password: admin
```

## API Documentation

- The API is documented using the OpenAPI standard.
- Access the API documentation by running the server and navigating to http://localhost:8001/api/doc/swagger/
  or http://localhost:8001/api/doc/redoc/.