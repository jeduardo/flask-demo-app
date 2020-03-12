# Flask demo app

This is a small demo app created in Flask created to exercise automated deployments
of non-trivial applications.

* Configuration based on environment variables
* Database-backed entries
* JSON API
* Stateless
* Support for X-Request-ID header for request tracking
* Logging with JSON to stdout

## Model

The only model defined for the application is the model of an `Entry`.

An `Entry` is composed by the following fields:
	* id: unique identifier for an entry. This field is generated automatically 
	and	cannot be modified.
	* description: a description for the `Entry`. 
	* comment: a comment over the `Entry`. 

## Configuration

The following environment variables can be configured:

* APP_DATABASE_URI (mandatory): points to the backing database.
* APP_LOG_LEVEL (optional): allows configuring the application log level. If it is
not specified, the default log level will be INFO.
* APP_HOST (optional): specifies which IP the application should bind to. If not
specified, it will bind to all addresses. T
* APP_PORT (optional): specified which port the application should bind to. If not
specified, it will bind to 5000.

## Deployment

The requirements for the application are listed in `requirements.txt`.

A PostgreSQL development package (such as `libpq-dev`) is required for pip to
compile the `psycopg2` dependency.

## API

The following endpoints are offered:

* /api/v1/entries
	* parameters: none
	* methods: GET
	* description: list all entries in the database
	* accepts: all formats
	* returns: application/json

* /api/v1/entries
	* parameters: JSON object representing an `Entry`
	* methods: POST
	* description: create a new entry
	* accepts: application/json
	* returns: application/json

* /api/v1/entries/<id>
	* parameters: JSON object representing an `Entry`
	* methods: POST
	* description: update an existing `Entry`
	* accepts: application/json
	* returns: application/json

* /api/v1/entries/<id>
	* parameters: entry id
	* methods: DELETE
	* description: remove an entry from the database
	* accepts: all formats
	* returns: application/json

* /api/v1/status
	* parameters: none
	* methods: GET
	* description: return "OK" if the application is reachable
	* accepts: all formats
	* returns: application/json

# License

This code is licensed under the MIT License.
