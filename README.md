# Personal Homepage
Fullstack using Fast-Api and Next.js

Table of Contents
-   [Running](#running)
    -   [Flask Locally](#flask-locally)
    -   [Next.js Locally](#nextjs-locally)
-   [Docker](#docker)
-   [Contributors](#contributors)

## Setup
A `.env` file is required for the supabase connection.
Under the root directory, create a .env file. This requires 2 values:
*   SUPABASE_URL
*   SUPABASE_KEY

Both of the values are found under the project settings in supabase

## Running

### Fastapi Locally
Working Directory needs to be `backend`

> uvicorn run:app --host 0.0.0.0 --port 4000
> uvicorn run:app --host 0.0.0.0 --port 4000 --reload

### Next.js Locally
Working Directory needs to be `frontend`

> npm run dev

## Docker
[Docker](https://www.docker.com/) must be installed in order to build the images

Working Directory needs to be `Personal-Homepage`

#### *Build*
> docker compose build

#### *Fast*
Building just the flask app
> docker compose up -d fastapp

#### *Next.js*
Building just the next app
> docker compose up -d nextapp

#### *Updating*
Following command will remove both the next and flask images and containers. Then rebuild and start both services
> docker compose down --rmi all && docker compose up --build

If you want to just update an individualy service, you need to manually remove the respective image and container. Then run the build command.

## Contributors

-   [Marc Ebersberger](https://github.com/BlueMonkeyQ)
-   [Andrue Desmarais](https://github.com/AndrueGage)
