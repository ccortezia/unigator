# The database layer

## Overview

Components in this layer offer different concrete implementations of use cases through exposition of database objects (tables, views, functions and triggers). All database implementations are meant to support the same set of use cases, even if internally different techniques are used or if they result in different performance profiles. Those differences are legit as long as all implementations comply to the public behavioral and structural contract defined in this document.

## Directory Layout

All components in this layer must comply to this directory layout:

```
- <dbfamily>-<version>
   + - api: programmatic data-access APIs
   + - ddl: data definition language sql files (schemas)
   + - dql: data query language sql files (operations)
   + - dml: data modification language files (base data)
   + - bin: database bootstrap scripts
```

## Operations Interface

_This section should be expanded as more database implementations are added. For now, postgresql-9.4 should be considered the reference. Documentation here is secondary in comparison to the layer-specific tests. They should act as live docs and enforce all constraints._
