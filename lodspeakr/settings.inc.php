<?php

$conf['endpoint']['local'] = 'http://localhost:8890/sparql';
$conf['home'] = '/var/www/abstracts/lodspeakr/';
$conf['basedir'] = 'http://198.61.161.98/abstracts/';
$conf['debug'] = false;
$conf['ns']['agu'] = 'http://abstracts.agu.org/ontology#';
$conf['ns']['local'] = 'http://abstracts.agu.org/';
$conf['ns']['base'] = 'http://198.61.161.98/abstracts/';
$conf['ns']['tw'] = 'http://tw.rpi.edu/schema/';

$conf['mirror_external_uris'] = $conf['ns']['local'];

//Variables in  can be used to store user info.
//For examples, 'title' will be used in the header
//(you can forget about all conventions and use your own as well)
$conf['modules']['available'] = array('static','uri', 'type', 'service');

$conf['root'] = '/abstracts/about/';
$lodspk['defaultGraph'] = 'http://abstracts.agu.org';
$lodspk['title'] = 'AGU Abstract Browser';
$lodspk['betaTitle'] = 'AGU Abstract Browser <sub>Beta</sub>';
$lodspk['maxResults'] = 500;
$lodspk['pagingLimit'] = 50;
?>