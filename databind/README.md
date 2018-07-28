# The databind layer

## Overview

Components in this layer are meant to provide language specific access to data objects provided by the underlying database layer, according to the public behavioral and structural contract defined in that layer. Currently two families of databinds are expected for any language: `sql` and `orm`. The most important point to note here is that a databind is not allowed to host specific use case logic. The only type of logic a databind is allowed to host is that of data type adaptations (to fulfill the expectations of its exposed interface while working around the limitations of the underlying data component and driver of choice).

## Pure SQL databinds

Databinds in the `sql` family shall rely only in:
- the standard sql operations as provided by the respective database component
- its language specific database driver of choice

_NOTE: a strict API for this family may be added here at some point. Until then, consider `py-sql` as a reference._

## ORM databinds

Databinds in the `orm` family shall rely only in:
- its database mapper definitions
- its language specific database driver of choice
