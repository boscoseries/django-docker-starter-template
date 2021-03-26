# USSD API v3.1

## Build the image

`docker-compose build`

## Run the container

`docker-compose up -d`

## Build the new image and spin up the two containers -- Use this more often

`docker-compose up -d --build`

## Run the migrations


`docker-compose exec web python manage.py migrate --noinput`

Get the following error?
`django.db.utils.OperationalError: FATAL: database "hello_django_dev" does not exist`

Run `docker-compose down -v` to remove the volumes along with the containers. Then, re-build the images, run the containers, and apply the migrations.

## Inspect the database

`docker-compose exec db psql --username=dbUser --dbname=dbName`

## You can check that the volume was created as well by running:

`docker volume inspect app_postgres_data`

## Update the file permissions locally

`chmod +x entrypoint.sh`

## Bring down the development containers (and the associated volumes with the -v flag) when you want to spin up the production images

`docker-compose down -v`

Then, build the production images and spin up the containers:

`docker-compose -f docker-compose.prod.yml up -d --build`

## Check error logs

`docker-compose -f docker-compose.prod.yml logs -f`

## Production Considerations

Here, we used a Docker [https://docs.docker.com/develop/develop-images/multistage-build/](multi-stage) build to reduce the final image size. Essentially, builder is a temporary image that's used for building the Python wheels.
The wheels are then copied over to the final production image and the builder image is discarded.
You could take the [https://stackoverflow.com/questions/53093487/multi-stage-build-in-docker-compose/53101932#53101932](multi-stage build) approach a step further and use a single Dockerfile instead of creating two Dockerfiles.
Think of the pros and cons of using this approach over two different files.

Did you notice that we created a non-root user?
By default, Docker runs container processes as root inside of a container.
This is a bad practice since attackers can gain root access to the Docker host if they manage to break out of the container.
If you're root in the container, you'll be root on the host.

## Production Build

`docker-compose down -v`

`docker-compose -f docker-compose.prod.yml down -v`

`docker-compose -f docker-compose.prod.yml up -d --build`

`docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput`

`docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear`
