# The database layer

## Overview

Components in this layer offer different concrete implementations of use cases through exposition of database objects (tables, views, functions and triggers). All database implementations are meant to support the same set of use cases, even if internally different techniques are used or if they result in different performance profiles. Those differences are legit as long as all implementations comply to the public behavioral and structural contract defined in this document.

## Directory Layout

All components in this layer must comply to this directory layout:

```
- <dbfamily>-<version>
   + - ddl: data definition language sql files (schemas)
   + - dql: data query language sql files (operations)
   + - dml: data modification language files (base data)

- <dbfamily>-default: symlink to the a specific default db version for the family

- <dbfamily>-common: files and templates common to all versions of a given dbfamily
   + - db-setup: performs initial database setup to allow for minimal tests (users, roles)
   + - db-reset: wipes out all data, rebuild schema and adds initial mandatory objects

- tests: generic database layer tests
   + - tests_dql: tests targeting database integrity
   + - tests_perf: tests targeting database performance

```

## Operations Interface

_This section should be expanded as more database implementations are added. For now, postgresql-9.4 should be considered the reference. Documentation here is secondary in comparison to the layer specific tests. They should act as live docs and enforce all constraints._
