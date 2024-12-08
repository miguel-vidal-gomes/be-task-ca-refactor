# Backend Task - Clean Architecture

This project is a very naive implementation of a simple shop system. It mimics in its structure a real world example of a service that was prepared for being split into microservices and uses the current Helu backend tech stack.

## Goals

Please answer the following questions:

1. Why can we not easily split this project into two microservices?

> The main reason lies in the way the components are tightly coupled. For example, the business logic (usecases) directly depends on the repository layer without proper abstraction. This dependency makes it difficult to isolate responsibilities into separate services. Additionally, the shared data models used across layers—such as the same User model for the API, domain, and persistence layers—entangle the modules. If you tried to split the project into two microservices (e.g., one for users and one for items), you'd have to significantly refactor these shared dependencies, which currently lack clear boundaries.

2. Why does this project not adhere to the clean architecture even though we have seperate modules for api, repositories, usecases and the model?

>While the project is organized into modules, the dependency flow doesn't align with clean architecture principles. In clean architecture, the inner layers (like domain models and usecases) should be independent of the outer layers (like repositories and the API). Here are the main issues:
>>- Lack of Dependency Inversion: The usecases directly depend on concrete implementations of the repositories. This makes it harder to replace or extend these components
>>- Coupled Data Models: The same data model is reused across layers, which blurs the boundaries between them. For instance, the database schema and API schema overlap, which is a clear violation of separation of concerns.
>>- Implementation Leakage: Details of persistence or transport mechanisms (like SQLAlchemy or FastAPI) leak into layers where they shouldn’t exist. For example, domain models might carry database-specific annotations or constraints.

3. What would be your plan to refactor the project to stick to the clean architecture?

>To bring this project in line with clean architecture principles, I’d recommend the following steps:
>>- Introduce Interfaces: Define clear interfaces for the repository layer. This will decouple the usecases from specific implementations (e.g., SQL, in-memory).
>>- Separate Data Models: Use different models for each layer. For example:
>>>- Domain models: Represent the core business logic.
>>>- Persistence models: Handle database-specific requirements.
>>>- API schemas: Define the structure of incoming and outgoing HTTP requests.
>>- Implement Dependency Injection: Use a dependency injection framework to pass dependencies into components dynamically, making the code more flexible and testable.
>>- Reorganize Responsibilities: Ensure that each layer is responsible for only one thing:
The API layer should handle HTTP requests and responses.
Usecases should contain only business logic.
Repositories should strictly manage data access.
>>- Modularize Microservices: As a long-term goal, consider encapsulating users and items into their own bounded contexts, complete with dedicated APIs, repositories, and models.

4. How can you make dependencies between modules more explicit?

>Here's a proposal:
>>- Use Explicit Contracts: Introduce interfaces or abstract base classes for repositories and services. This will document the interactions between layers and ensure that the implementation adheres to a defined contract.
>>- Visualize Dependencies: Use tools or diagrams to map out the relationships between modules. This helps to identify and reduce unnecessary coupling.
>>- Adopt Dependency Injection: Explicitly pass dependencies into components via constructors or dependency injection frameworks. This ensures that dependencies are visible and configurable.
>>- Enforce Layered Boundaries: Use static analysis tools or linters to enforce architectural rules, ensuring that dependencies flow in the correct direction (from outer layers to inner layers).

>By addressing these points, the project can achieve a cleaner, more maintainable structure that adheres to the principles of clean architecture while also becoming easier to scale and refactor in the future.

*Please do not spend more than 2-3 hours on this task.*

Stretch goals:
* Fork the repository and start refactoring
* Write meaningful tests
* Replace the SQL repository with an in-memory implementation

## References
* [Clean Architecture by Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
* [Clean Architecture in Python](https://www.youtube.com/watch?v=C7MRkqP5NRI)
* [A detailed summary of the Clean Architecture book by Uncle Bob](https://github.com/serodriguez68/clean-architecture)

## How to use this project

If you have not installed poetry you find instructions [here](https://python-poetry.org/).

1. `docker-compose up` - runs a postgres instance for development
2. `poetry install` - install all dependency for the project
3. `poetry run schema` - creates the database schema in the postgres instance
4. `poetry run start` - runs the development server at port 8000
5. `/postman` - contains an postman environment and collections to test the project

## Other commands

* `poetry run graph` - draws a dependency graph for the project
* `poetry run tests` - runs the test suite
* `poetry run lint` - runs flake8 with a few plugins
* `poetry run format` - uses isort and black for autoformating
* `poetry run typing` - uses mypy to typecheck the project

## Specification - A simple shop

* As a customer, I want to be able to create an account so that I can save my personal information.
* As a customer, I want to be able to view detailed product information, such as price, quantity available, and product description, so that I can make an informed purchase decision.
* As a customer, I want to be able to add products to my cart so that I can easily keep track of my intended purchases.
* As an inventory manager, I want to be able to add new products to the system so that they are available for customers to purchase.