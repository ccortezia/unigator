# The controller layer

## Overview

Components in this layer are primarily meant to offer sane ways for driver applications to manipulate the database layer through one or more databinds. The services offered by controllers may comprise higher level patterns and abstractions, but that is not a must. Controllers may make themselves reachable remotely by offering an inter-process RPC API, or they may be limited to intra-process API.

_TODO: spec a common interface for all controllers, to determine mandatory public functionality_
