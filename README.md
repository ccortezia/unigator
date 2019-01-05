# Unigator

[![CircleCI](https://circleci.com/gh/ccortezia/unigator/tree/master.svg?style=svg)](https://circleci.com/gh/ccortezia/unigator/tree/master)

A database-centered Physical Access Control System.

## Overview

Unigator is a data-centered implementation of typical use cases related to granting people selective physical access to areas. A typical access flow is comprised of at least 3 steps: attempt classification, authorization evaluation, history consolidation. From that central idea stem all the domain modelling for Unigator.

## Additional Information

- [Use Cases](docs/use-cases.md): the primary list of covered real-world use cases.
- [Domain Driven Design](docs/ddd.md): the business domain reduced to its essentials.
- [System Architecture](docs/architecture.md): the overall solution exposed at a high level.
- [Design Principles](docs/design.md): the core values behind all technical decisions.

## Directory Layout

- [terminal](terminal/README.md): programs meant to allow humans to interact with the system.
- [controller](controller/README.md): programs and libraries to support use cases end to end.
- [databind](databind/README.md): libraries to provide direct access to database objects.
- [database](database/README.md): database schemas and queries to support use cases.
- [physical](physical/README.md): programs and libraries that offer access to physical devices.
- [stack](stack/README.md): docker-compose files for the various stack combinations.

## Running Locally

This project is designed to provide the pieces to compose different solutions and to be deployment agnostic. For development and testing purposes though, it uses docker-compose to facilitate the launch and exploration of different compositions. The example below illustrates the stack composition launch of the default postgresql standalone stack:

```shell
docker-compose -p unigator -f stack/pg up -d

export PGPORT=5432
export PGHOST=localhost
PGUSER=postgres database/postgresql-common/db-setup
PGUSER=unigator database/postgresql-common/db-reset default
PGPASSWORD=123123 psql -h localhost -U unigator -c 'select * from ung.ac_contacts;'
```

Once the above steps are complete, try running one of the examples found [here](docs/examples.md).

## Running Tests

```shell
# Prepare a test runner image
docker build . -f .circleci/Dockerfile -t testrunner

# Launch a target stack
docker-compose -f stack/pg -d

# Launch a test runner attached to the stack's network
docker run --network unigator --rm -it testrunner
```

## Roadmap

- Fill design doc
- Fill architecture doc
- Fill use cases doc
- Improve examples doc
- Top level Makefile to drive build & tests
- Refactor circleci config: improve blocks reuse, parametrization
- Implement proper database performance tests: requires cached massive datasets
- Generalise test running: parametrize for multiple stacks
- Improve/generalise dql/operations.sql (requires improved anosql)
- Generalize database test code: pytest tagging for common x specific-db tests
- Implement controller/py-http-api
- Implement terminal/go-admin-cli
