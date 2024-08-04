# DIY Vector Tile Server with FastAPI and PostGIS

Build your own dynamic vector tile server with FastAPI, PostGIS and Async SQLAlchemy quickly and easily.

To run the services do `./scripts/run.sh dev`, this will:

- start the Postgres Docker container
- create the database and `listing`, import the data and create the indexes
- start the FastAPI server

Once the services are running, you can access HTML Map template at at `http://localhost:8000/` that fetches the vector tiles at `http://localhost:8000/listings/tiles/{z}/{x}/{y}.mvt`.