# Personal Homepage
Fullstack using Flask and Next.js

Table of Contents
-   [Running](#running)
    -   [Flask Locally](#flask-locally)
    -   [Next.js Locally](#nextjs-locally)
-   [Docker](#docker)
-   [Contributors](#contributors)

## Running

### Flask Locally
Working Directory needs to be `backend`

> flask --app run --debug run --host=0.0.0.0 --port=4000

### Next.js Locally
Working Directory needs to be `frontend`

> npm run dev

## Docker
[Docker](https://www.docker.com/) must be installed in order to build the images

Working Directory needs to be `Personal-Homepage`

#### *Build*
> docker compose build

#### *Flask*
> docker compose up -d flaskapp

#### *Next.js*
> docker compose up -d nextapp

#### *Updating*
If you want new code in your docker image, you need to delete both the container and the image, then run the compose command again to build the new image and container

## Contributors

-   [Marc Ebersberger](https://github.com/BlueMonkeyQ)
-   [Andrue Desmarais](https://github.com/AndrueGage)
