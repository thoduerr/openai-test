# Development Goal
Create a comprehensive example of a microservice using the latest version of Quarkus.io that includes CRUD operations.

## Functional Requirements
- **CRUD Operations**: Implement Create, Read, Update, and Delete functionalities for an entity named `Thing`, which has complex attributes.

## Architecture

### Design: Follow hexagonal and clean architecture principles with distinct components for:
  - Domain Logic: Include input and output ports.
  - Data Storage: Implement interactions with MongoDB.

### Role-Based Access Control
- **Roles**:
  - **Admin (Anna)**: Full access to all operations.
  - **Editor (Eric)**: Can create, read, and update.
  - **Reader (Ron)**: Read-only access.
- **Authentication**: Utilize a custom attribute in the JWT access token to assign roles.

### Security and Documentation
- **Security**: Ensure all endpoints are secure.
- **Documentation**: Provide comprehensive documentation of the REST API.
- **Logging**: Implement logging at the entry and exit of methods and maintain security at all levels.

### Deployment
- **Containerization**: Deploy using containers managed by Podman.

## Development
- Prereqs: java, IDE, quarkus, database, podman
- Installation & Setup
- Configuration for development and production (secure)
- Testing: Unit tests and Integration Tests
- end to end example

## Expected Deliverables
- A fully functional microservice architecture example.
- Source code and architectural diagrams.
- Accessible API documentation for integration and testing purposes.
