# Unigator

[![CircleCI](https://circleci.com/gh/ccortezia/unigator/tree/master.svg?style=svg)](https://circleci.com/gh/ccortezia/unigator/tree/master)

A database-centered Physical Access Control System.

## Overview

Unigator is a data-centered implementation of typical use cases related to granting people selective physical access to areas. A typical access flow is comprised of at least 3 steps: attempt classification, authorization evaluation, history consolidation. From that central idea stem all the domain modelling for Unigator.

## Additional Information

- [Use Cases](docs/use-cases.md): the primary list of covered real-world use cases.
- [Domain Model](docs/ddd.md): the business domain reduced to its essentials.
- [System Architecture](docs/architecture.md): the overall solution exposed at a high level.
- [Design Principles](docs/design.md): the core values behind all technical decisions.

## Directory Layout

- [terminal](terminal/README.md): programs meant to allow humans to interact with the system.
- [controller](controller/README.md): programs and libraries to support use cases end to end.
- [database](database/README.md): database schemas and queries to support use cases.
- [physical](physical/README.md): programs and libraries that offer access to physical devices.
- [stack](stack/README.md): docker-compose files for the various stack combinations.

## Running Locally

```shell
make stack.pg.start.d
make db.pg.setup
make db.pg.reset
make db.pg.query QUERY='select * from ung.ac_contacts;'
```

See more examples [here](docs/examples.md).

## Running Tests

Run the CI sequence locally:

```shell
make test.ci
```

Run tests against a locally-running stack:

```shell
make stack.pg.start.d && make test
```

## Roadmap

- Fill design doc
- Fill architecture doc
- Fill use cases doc
- Improve examples doc
- Refactor circleci config: improve blocks reuse, parametrization
- Implement proper database performance tests: requires cached massive datasets
- Generalise test running: parametrize for multiple stacks
- Generalize database test code: pytest tagging for common x specific-db tests
- Implement controller/py-http-api
- Implement terminal/go-admin-cli
