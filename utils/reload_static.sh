#!/bin/bash

LOAD=./virtuoso/vload
DELETE=./virtuoso/vdelete
RDFDIR=/data/abstracts/rdf
STATIC=http://abstracts.agu.org/graphs/2.0/static

$DELETE $STATIC
$LOAD ttl $RDFDIR/static.ttl $STATIC
