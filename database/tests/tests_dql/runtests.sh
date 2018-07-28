#!/bin/bash

set -e
set -u

readonly HERE="$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)"
readonly DSPATH=$HERE/../../../databind/py-sql/

PGUSER=unigator PGHOST=localhost PYTHONPATH=$DSPATH py.test -s $@
