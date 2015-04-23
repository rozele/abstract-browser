#!/bin/bash

CODE=${1:0:4}
sed -e "s/src=\"images/src=\"http:\/\/www.agu.org\/meetings\/${CODE}\/program\/images/g" < ${1} > tmpfile
sed -e "s/src=\"tables/src=\"http:\/\/www.agu.org\/meetings\/${CODE}\/program\/tables/g" < tmpfile > ${1}
rm tmpfile
