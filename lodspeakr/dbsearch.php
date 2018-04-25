<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>AGU Abstract Browser</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
    <link href="http://abstractsearch.agu.org/css/bootstrap.min.css" rel="stylesheet" type="text/css" media="screen" />
    <style>
        html, body {
            height: 100%;
            min-width: 350px;
        }
        footer {
            height: auto;
            width: auto;
            color: #666;
            background: #222;
            padding: 5px 0 0px 0;
            border-top: 1px solid #000;
            text-align: center;
        }
        footer a {
            color: #999;
        }
        footer a:hover {
            color: #efefef;
        }
        .wrapper {
            min-height: 100%;
            height: auto !important;
            height: 100%;
            margin: 0 auto -40px;
        }
        .push {
            height: 40px;
        }
        /* not required for sticky footer; just pushes hero down a bit */
        .wrapper > .container {
            padding-top: 0px;
        }
        .push-bottom {
            margin-bottom: 2ex;
        }
    </style>
    <link href="http://abstractsearch.agu.org/css/bootstrap-responsive.min.css" rel="stylesheet" type="text/css" media="screen" />
    <script type="text/javascript" src="http://abstractsearch.agu.org/js/jquery.js"></script>
    <script type="text/javascript" src="http://abstractsearch.agu.org/js/bootstrap.min.js"></script>
    <script type="text/javascript" src="http://abstractsearch.agu.org/js/bootstrap-typeahead.js"></script>
    <script type="text/javascript">
    function bifConvert(query) {
      var arr = query.split(" ");
      var i = 0
      for (; i < arr.length - 1; ++i) {
        arr[i] = '"' + arr[i] + '"';
      }
      if (arr[i].length > 4) {
        arr[i] = arr[i] + "*";
      }
      arr[i] = '"' + arr[i] + '"';
      return arr.join("%20AND%20");
    }

    function refreshPaging(count) {
      if (document.location.href.match(/limit=(\d+)/gi) != null) {
        var tmploc = document.location.href.replace(/&limit=\d*/gi, "&limit=" + count);
        window.location = tmploc.replace(/&offset=\d*/gi, "&offset=0");
      } 
      else {
        window.location = document.location.href + "&limit=" + count;
      }
    }

    $(document).ready(function(){
        /*$('.typeahead').typeahead({
            source: function (typeahead, query) {
              $('.typeahead').addClass('wait');[]
              
              return $.get('http://abstractsearch.agu.org/search/'+bifConvert(query), { }, function (data) {
                  $('.typeahead').removeClass('wait');[]
                  return typeahead.process(data);
              }, 'json');
            },
            onselect: function (obj) {
              $('.typeahead').attr('disabled', true);
              window.location = obj.uri;
            }
        });*/
        var match = document.location.href.match(/limit=\d*/gi);
        if (match != null) {
          var count = match[0].split("=")[1];
          $("#limitsel").find("option").removeAttr("selected");
          $("#limitsel").find("option[value="+count+"]").attr("selected","selected");
        }               
    });
    </script>
  </head>
  <body>
    <div class="wrapper">
      <div class="navbar">
        <div class="navbar-inner">
          <div class="container">
            <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
            </a>
            <a class="brand" href="http://abstractsearch.agu.org/"><span>AGU Abstract Browser</span></a>
            <div class="nav-collapse">
              <ul class="nav">
                <li><a href="http://abstractsearch.agu.org/">About</a></li>
                <!--<li><a href="http://abstractsearch.agu.org/classes">Classes</a></li>-->
                <!--<li><a href="http://abstractsearch.agu.org/namedGraphs">Named Graphs</a></li>-->
                <li><a href="http://abstractsearch.agu.org/meetings">Meetings</a></li>
                <li><a href="http://abstractsearch.agu.org/vps">Virtual Posters</a></li>
                <!--<li><a href="http://abstractsearch.agu.org/people">Authors</a></li>-->
                <li><a href="http://abstractsearch.agu.org/sections">Sections</a></li>
                <li><a href="http://abstractsearch.agu.org/keywords">Index Terms</a></li>
                <!--<li><a href="http://abstractsearch.agu.org/dbsearch.php">Advanced Search</a></li>-->
              </ul>
              <form class="navbar-search pull-left" action="">
                <input type="text" data-provide="typeahead" name="q[]" class="typeahead search-query span2" placeholder="Quick Search"/>
                <input type="hidden" name="field[]" value="all" />
                <input class="btn" type="submit" />
              </form>
            </div><!--/.nav-collapse -->
          </div>
        </div>
      </div>
      <div class="container-fluid push-bottom">
        <div id="banner">
	  <!--<a href="http://sites.agu.org/"><img src="http://abstractsearch.agu.org/images/agu_logo_blue.png" alt="AGU - Earth | Oceans | Atmosphere | Space | Planets" title="AGU - Earth | Oceans | Atmosphere | Space | Planets" height="100em" hspace="0" vspace="0" border="0" align="top" usemap="#Map"></a>-->        
	</div>
        <h2>Search Results</h2>
<?php
$prefixes = array(
  "swrc" => "http://swrc.ontoware.org/ontology#",
  "dc" => "http://purl.org/dc/terms/",
  "swc" => "http://data.semanticweb.org/ns/swc/ontology#",
  "tw" => "http://tw.rpi.edu/schema/",
  "foaf" => "http://xmlns.com/foaf/0.1/",
  "agu" => "http://abstractsearch.agu.org/ontology#",
  "void" => "http://rdfs.org/ns/void#"
);

$fields = array(
  "all" => "All Fields",
  "abstract" => "Abstract",
  "abstitle" => "Abstract Title",
  "abscode" => "Abstract Number",
  "keyword" => "Index Term",
  "author" => "Author Name",
  "email" => "Author E-mail",
  "affiliation" => "Author Affiliation",
  "sid" => "Session Code",
  "session" => "Session Title",
  "convener" => "Convener Name",
  "meeting" => "Meeting Name",
  "mtgyear" => "Meeting Year",
  "mtgcode" => "Meeting Code",
  "section" => "Section Name",
  "scode" => "Section Code"
);

$contains = array(
  "abstract" => "?abstract swrc:abstract {var} . ",
  "abstitle" => "?abstract dc:title {var} . ",
  "all" => "?abstract agu:raw {var} . ",
);

$filter = array(
  "abstract" => "?abstract swrc:abstract {var} . ",
  "abstitle" => "?abstract dc:title {var} . ",
  "all" => "?abstract agu:raw {var} . ",
  "keyword" => "?keyword a swrc:ResearchTopic . { ?keyword dc:subject {var} } UNION { ?keyword dc:identifier {var} } ",
  "author" => "?author a foaf:Person . ?author tw:hasRole ?role . ?author foaf:name {var} . ",
  "affiliation" => "?affiliation a foaf:Organization . ?affiliation dc:description {var} . ",
  "session" => "?session a swc:SessionEvent . ?session swrc:eventTitle {var} . ",
  "convener" => "?convener a foaf:Person . ?convener tw:hasRole ?role . ?convener foaf:name {var} . ",
  "meeting" => "?meeting a swrc:Meeting . ?meeting swrc:eventTitle {var} . ",
  "section" => "?section dc:title {var} . ",
);

$exact = array(
  "abscode" => "?abstract dc:identifier {exact} . ",
  "email" => array("?author a foaf:Person . ?author tw:hasRole ?role . ?author foaf:mbox {exact} . ", "xsd:string"),
  "sid" => "?session a swc:SessionEvent . ?session dc:identifier {exact} . ",
  "mtgyear" => array("?meeting a swrc:Meeting . ?meeting swrc:year {exact} . ", "xsd:gYear"),
  "mtgcode" => array("?meeting a swrc:Meeting . ?meeting agu:meetingCode {exact} . ", "xsd:string"),
  "scode" => array("?section dc:identifier {exact} . ", "xsd:string")
);

$link = array(
  "keyword" => array("?abstract swc:hasTopic ?keyword . "),
  "author" => array("?abstract tw:hasAgentWithRole ?role . "),
  "email" => array("?abstract tw:hasAgentWithRole ?role . "),
  "affiliation" => array("?abstract tw:hasAgentWithRole ?role . ", "?role tw:withAffiliation ?affiliation . "),
  "sid" => array("?abstract swc:relatedToEvent ?session . "),
  "session" => array("?abstract swc:relatedToEvent ?session . "),
  "convener" => array("?abstract swc:relatedToEvent ?session . ", "?session tw:hasAgentWithRole ?role . "),
  "meeting" => array("?abstract swc:relatedToEvent ?session . ", "?session swc:isSubEventOf ?meeting . "), 
  "mtgyear" => array("?abstract swc:relatedToEvent ?session . ", "?session swc:isSubEventOf ?meeting . "),
  "mtgcode" => array("?abstract swc:relatedToEvent ?session . ", "?session swc:isSubEventOf ?meeting . "),
  "section" => array("?abstract swc:relatedToEvent ?session . ", "?session agu:section ?section . "),
  "scode" => array("?abstract swc:relatedToEvent ?session . ", "?session agu:section ?section . ")
);

$graphns = "http://abstractsearch.agu.org/graphs/2.0";
$metagraph = "$graphns/static";

$graphType = array(
  "all" => "?g",
  "abstract" => "?g",
  "abstitle" => "?g",
  "abscode" => "?g",
  "keyword" => "<$graphns/keywords>",
  "author" => "<$graphns/people>",
  "email" => "<$graphns/people>",
  "affiliation" => "<$graphns/organizations>",
  "sid" => "?g",
  "session" => "?g",
  "convener" => "?g",
  "meeting" => "?g",
  "mtgyear" => "?g",
  "mtgcode" => "?g",
  "section" => "?g",
  "scode" => "?g"
);

//$sparql["all"] = "{ " . implode(" } UNION { ", array_values($sparql)) . " }";

$boolopt = array("and","or");
$debug = getDebug();
$useGraphs = false;

function sparqlSelect($query, $endpoint = "http://localhost:8890/sparql")
{
  global $debug;
  if ($debug) { echo htmlspecialchars($query) . "<br/>"; return; }
  $curl = curl_init();
  curl_setopt($curl, CURLOPT_URL, $endpoint);
  curl_setopt($curl, CURLOPT_POST, true);
  curl_setopt($curl, CURLOPT_POSTFIELDS, getQueryData($query));
  curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
  $content = curl_exec($curl);
  curl_close($curl);
  $xml = simplexml_load_string($content);
  $results = array();
  foreach ($xml->results->result as $result) {
    $arr = array();
    foreach($result->binding as $binding) {
      $name = $binding['name'];
      $arr["$name"] = (string) $binding->children();
    }
    array_push($results,$arr);
  }
  return $results;
}

function getQueryData($query, $suffix = '') {
  return 'query='.urlencode($query).'&format=xml'.$suffix;
}

function buildPrefixes() {
  global $prefixes;
  $q = "";
  foreach ($prefixes as $prefix => $uri) {
    $q .= "PREFIX $prefix: <$uri> ";
  }
  return $q;
}

function buildGraphs($disjunctions) {
  global $metagraph, $graphns, $graphType;
  foreach ($disjunctions as $i => $d)
  {
    foreach ($d as $j => $s)
    {
      if ($graphType[$s[1]] == "?g")
      {
        return "GRAPH <$metagraph> { <$graphns> void:subset ?g } ";
      }
    }
  }
  return "";
}

function buildQuery($disjunctions, $limit, $offset, $counting = false) {
  global $filter, $contains, $exact, $link, $metagraph, $graphns, $useGraphs, $graphType;
  $q = buildPrefixes();
  $q .= (!$counting) ? "SELECT DISTINCT ?abstract MAX(?mtitle) as ?title ?id ?code MAX(?myear) as ?year WHERE { " : "SELECT (count(DISTINCT ?abstract) as ?count) WHERE { ";
  if ($useGraphs) $q .= buildGraphs($disjunctions);
  $linked = array();
  foreach ($disjunctions as $i => $d) {
    $union = array();
    foreach ($d as $j => $s) {
      $g = $graphType[$s[1]];
      if (array_key_exists($s[1], $contains) && count($disjunctions) == 1) {
        $pattern = "";
        if ($useGraphs) $pattern .= "GRAPH $g { ";
        $pattern .= $contains[$s[1]] . " {var} bif:contains '\"" . $s[0] . "\"' . ";
        if ($useGraphs) $pattern .= "} ";
        $union[] = $pattern;
      }
      else if (array_key_exists($s[1], $filter)) {
        $pattern = "";
        if ($useGraphs) $pattern .= "GRAPH $g { ";
        $pattern .= $filter[$s[1]] . " FILTER regex({var},\"" . $s[0] . "\",\"i\") ";
        if ($useGraphs) $pattern .= "} ";
        $union[] = $pattern;
      }
      else if (array_key_exists($s[1], $exact) && is_array($exact[$s[1]])) {
        $pattern = "";
        if ($useGraphs) $pattern .= "GRAPH $g { ";
        $pattern .= $exact[$s[1]][0] . " ";
        if ($useGraphs) $pattern .= "} ";
        $pattern = str_replace("{exact}", "\"" . $s[0] . "\"^^" . $exact[$s[1]][1], $pattern);
        $union[] = $pattern;
      }
      else if (array_key_exists($s[1], $exact) && !is_array($exact[$s[1]])) {
        $pattern = "";
        if ($useGraphs) $pattern .= "GRAPH $g { ";
        $pattern .= $exact[$s[1]] . " ";
        if ($useGraphs) $pattern .= "} ";
        $pattern = str_replace("{exact}", "\"" . $s[0] . "\"", $pattern);
        $union[] = $pattern;
      }
    }
    $c = implode(" UNION ",$union) . " ";
    $q .= str_replace("{var}","?l$i",$c); 
    if (array_key_exists($s[1], $link)) {
      foreach ($link[$s[1]] as $i => $l) {
        $linked[] = $l;
      }
    }
  }
  $bgps = array(
    "?abstract dc:title ?mtitle . ",
    "?abstract dc:identifier ?id . "
  );
  if (!$counting) $bgps = array_merge($bgps, array(
    "?abstract swc:relatedToEvent ?session . ",
    "OPTIONAL { ", # TN for VPS
    "?session swc:isSubEventOf ?meeting . ",
    "?meeting agu:meetingCode ?code . ",
    "?meeting swrc:year ?myear . ",
    "?meeting swrc:startDate ?start . ",
    "}" # TN for VPS
  ));
  $linked = array_unique(array_merge($linked, $bgps));
  $q .= implode("", $linked);
  $q .= "}";
  $q .= (!$counting) ? " ORDER BY desc(?start) ?abstract LIMIT $limit OFFSET $offset" : "";
  return $q;
}

function getFieldOptions() {
  global $fields;
  $str = "";
  foreach ($fields as $key => $title)
    $str .= "<option value=\"$key\">$title</option>";
  return $str;
}

function getBooleanOptions() {
  global $boolopt;
  $str = "";
  foreach ($boolopt as $i => $key)
    $str .= "<option>$key</option>";
  return $str;
}

function getArgc() {
  $count = 0;
  foreach ($_GET["q"] as $i => $q)
    if ($q && trim($q) != "") $count++;
  return $count;
}

function getDebug() {
  return array_key_exists("debug", $_GET);
}

function getPaging() {
  $limit = 50;
  if (isset($_GET["limit"]) && $_GET["limit"] != "") {
    $limit = intval($_GET["limit"]);
  }
  $offset = 0;
  if (isset($_GET["offset"]) && $_GET["offset"] != "") {
    $offset = intval($_GET["offset"]);
  }
  return array($limit,$offset);
}

function getUrl($limit,$offset,$next) {
  $filename = explode("/",__FILE__);
  $filename = $filename[count($filename) - 1];
  $qstring = $filename . "?";
  foreach ($_GET["q"] as $i => $q) {
    if ($i != 0) $qstring .= "&";
    $qstring .= "q%5B%5D=$q";
  }
  foreach ($_GET["field"] as $i => $f) {
    $qstring .= "&field%5B%5D=$f";
  }
  #foreach ($_GET["boolean"] as $i => $f) {
  #  if ($i != 0) $qstring .= "&";
  #  $qstring .= "&boolean%5B%5D=$f";
  #}
  $offset = ($next) ? $limit + $offset : $offset - $limit;
  $qstring .= "&limit=$limit&offset=$offset";
  return $qstring;
}

function getNextDisjunction($i,$argc) {
  $arr = array();
  for ($i; $i < 3; ++$i) {
    if ($_GET["q"][$i] != "") {
      $arr[] = array($_GET["q"][$i],$_GET["field"][$i]);
      if ($i == $argc - 1 || $_GET["boolean"][$i] != "or")
        break;
    } 
  }
  $i = ($i < 3) ? $i + 1 : $i;
  return array($i,$arr);
}

function printDisjunction($ds) {
  global $fields;
  $arr = array();
  foreach ($ds as $d) {
    $arr[] = '"' . $d[0] . '" in ' . $fields[$d[1]];
  }
  return implode(" or ",$arr);
}

function localize($url) {
  return substr($url,30);
}

$argc = getArgc();
$paging = getPaging();
$limit = $paging[0];
$offset = $paging[1];

if ($argc == 0) {
  echo "<br/><p>No query terms were entered</p>";
  #echo "<p>Enter query terms and select fields to search:</p>" .
  #  "<form action=\"dbsearch.php\">" .
  #  "<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type=\"text\" name=\"q[]\" /><br/>" .
  #  "<span>In&nbsp;&nbsp;<select name=\"field[]\">" . getFieldOptions() . "</select>&nbsp;&nbsp;" . 
  #  "<select class=\"input-small\" name=\"boolean[]\">" . getBooleanOptions(). "</select></span></p>" .
  #  "<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type=\"text\" name=\"q[]\" /><br/>" .
  #  "<span>In&nbsp;&nbsp;<select name=\"field[]\">" . getFieldOptions() . "</select>&nbsp;&nbsp;" . 
  #  "<select class=\"input-small\" name=\"boolean[]\">" . getBooleanOptions(). "</select></span></p>" .
  #  "<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type=\"text\" name=\"q[]\" /><br/>" .
  #  "<span>In&nbsp;&nbsp;<select name=\"field[]\">" . getFieldOptions() . "</select></span></p>" .
  #  "<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<input type=\"submit\" value=\"Search\"></p></form>" .
  #  "<p>For more information about each of the fields, check out the <a href=\"http://abstractsearch.agu.org/about/advsrch\">Advanced Search Field Overview</a>.</p>";
}

else {
  if ($argc > 0) {
    $i = 0;
    $disjunctions = array();
    $arr = array();
    $count = 0;
    while ($count < $argc) {
      $t = getNextDisjunction($i,$argc);
      $i = $t[0];
      $arr[] = printDisjunction($t[1]);
      $disjunctions[] = $t[1];
      $count++;
    }
    echo "<p><span><b>Search Query:</b> " . implode(" and ",$arr) . "</span></p>";
    $results = sparqlSelect(buildQuery($disjunctions,$limit,$offset));
    $count = sparqlSelect(buildQuery($disjunctions,null,null,true));
    $count = intval($count[0]["count"]);
    $startIndex = $offset + 1;
    if ($count && count($results) > 0) {
      $pagingInfo = "Showing Results ";
      $pagingInfo .= $startIndex . " - ";
      $pagingInfo .= ($offset + $limit < $count) ? $limit + $offset : $count;
      $pagingInfo .= " of $count"; 
      $pagingInfo .= ", <span>sorted by meeting date (decreasing), then abstract number.</span>";
    } else if ($count && count($results == 0)) {
      $pagingInfo = "Search query was too broad, finding $count results, please narrow your search.";
    } else {
      $pagingInfo = "No results found, please refine search terms.";
    }
    echo "<p><span><b>$pagingInfo</b></span></p><ol start=\"$startIndex\">";
    foreach ($results as $i => $result) {
      echo "<li><a href=\"" . localize($result["abstract"]) . "\">[" . $result["code"] . substr($result["year"],2,2) . "-" . $result["id"] . "] " . $result["title"] . "</a></li>";
    }
    echo "</ol>";
    echo "<span>";
    if ($offset > 0) {
      echo "<a href=\"" . getUrl($limit,$offset) .  "\"><button>Prev</button></a>";
    }
    if (count($results) > 0)
    {
      if ($offset || $offset + $limit < $count) echo " | ";
      if ($offset + $limit < $count) {
        echo "<a href=\"" . getUrl($limit,$offset,true) . "\"><button>Next</button></a>";
      }
      if ($count > $limit)
        echo " Results Per Page <select style=\"width:4.1em;vertical-align:middle\" id=\"limitsel\" onChange=\"refreshPaging(this.value)\"><option>10</option><option>20</option><option selected>50</option><option>100</option><option>200</option></select>";
      echo "</span>";
    }
  }
}

?>
      </div>
      <div class="push"><!--//--></div>
    </div>
    <footer class="navbar-inner">
      <span>Created by <a href="http://www.linkedin.com/pub/eric-rozell/22/638/48b/">Eric Rozell</a> and <a href="http://narock.github.io">Tom Narock</a>. Powered by <a href="http://lodspeakr.org/">LODSPeaKr</a>.</span>
    </footer>
  </body>
</html>
