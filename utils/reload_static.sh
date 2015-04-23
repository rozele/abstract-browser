#!/bin/bash

LOAD=/opt/virtuoso/scripts/vload
DELETE=/opt/virtuoso/scripts/vdelete
RDFDIR=../data/agu/rdf-1.0
STATIC=http://abstracts.agu.org/graphs/1.0/static

$DELETE $STATIC
$LOAD ttl $RDFDIR/static.ttl $STATIC
