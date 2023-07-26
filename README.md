
<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<div align="center">
  <h2>Webtronics</h2>
  <a href="https://webtronics.ru/">
    <img src="https://webtronics.ru/images/tild3962-3963-4065-b139-643766666461___1.svg" alt="Logo" width="400" height="100">
  </a>

  <h3 align="center">README тестового задания</h3>

  <p align="center">
    simple RESTful API using FastAPI for a social networking application
  </p>
</div>

<hr>

<!-- ABOUT THE PROJECT -->
## About The Project

Functional requirements:
* There should be some form of authentication and registration (JWT, Oauth, Oauth 2.0, etc..)
* As a user I need to be able to signup and login
* As a user I need to be able to create, edit, delete and view posts
* As a user I can like or dislike other users’ posts but not my own 
* The API needs a UI Documentation (Swagger/ReDoc)

Bonus section (not required):
* Use https://clearbit.com/platform/enrichment for getting additional data for the user on signup
* Use emailhunter.co for verifying email existence on registration
* Use an in-memory DB for storing post likes and dislikes (As a cache, that gets updated whenever new likes and dislikes get added) 

### Built With

* [![FastAPI][FastAPI-badge]][FastAPI-url]
* [![PostgreSQL][PostgreSQL-badge]][PostgreSQL-url]
* [![Docker][Docker-badge]][Docker-url]

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Copy project to repository on local machine
* HTTPS or SSH
  ```sh
  git clone https://github.com/SuperLalka/webtronics-test.git
  ```
  ```sh
  git clone git@github.com:SuperLalka/webtronics-test.git
  ```

### Installation

To start the project, it is enough to build and run docker containers.
Database migrations will be applied automatically

1. Build docker containers
   ```sh
   docker-compose -f docker-compose.yml build
   ```
2. Run docker containers
   ```sh
   docker-compose -f docker-compose.yml up -d
   ```

### Documentation

The project API documentation is located at

    http://0.0.0.0:8000/documentation/docs

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[FastAPI-badge]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com
[PostgreSQL-badge]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[Docker-badge]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
