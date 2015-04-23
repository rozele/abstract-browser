<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>AGU Abstract Browser</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
    <link href="http://198.61.161.98/abstracts/css/bootstrap.min.css" rel="stylesheet" type="text/css" media="screen" />
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
    <link href="http://198.61.161.98/abstracts/css/bootstrap-responsive.min.css" rel="stylesheet" type="text/css" media="screen" />
    <script type="text/javascript" src="http://198.61.161.98/abstracts/js/jquery.js"></script>
    <script type="text/javascript" src="http://198.61.161.98/abstracts/js/bootstrap.min.js"></script>
    <script type="text/javascript" src="http://198.61.161.98/abstracts/js/bootstrap-typeahead.js"></script>
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

    $(document).ready(function(){
        $('.typeahead').typeahead({
            source: function (typeahead, query) {
              $('.typeahead').addClass('wait');[]
              
              return $.get('http://198.61.161.98/abstracts/search/'+bifConvert(query), { }, function (data) {
                  $('.typeahead').removeClass('wait');[]
                  return typeahead.process(data);
              }, 'json');
            },
            onselect: function (obj) {
              $('.typeahead').attr('disabled', true);
              window.location = obj.uri;
            }
        });
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
            <a class="brand" href="http://198.61.161.98/abstracts/"><span>AGU Abstract Browser <sub>Beta</sub></span></a>
            <div class="nav-collapse">
              <ul class="nav">
                <li><a href="http://198.61.161.98/abstracts/">Home</a></li>
                <!--<li><a href="http://198.61.161.98/abstracts/classes">Classes</a></li>-->
                <!--<li><a href="http://198.61.161.98/abstracts/namedGraphs">Named Graphs</a></li>-->
                <li><a href="http://198.61.161.98/abstracts/meetings">Meetings</a></li>
                <!--<li><a href="http://198.61.161.98/abstracts/people">Authors</a></li>
                <li><a href="http://198.61.161.98/abstracts/keywords">Keywords</a></li>-->
                <li><a href="http://198.61.161.98/abstracts/sections">Sections</a></li>
                <li><a href="http://198.61.161.98/abstracts/dbsearch.php">Advanced Search</a></li>
              </ul>
              <form class="navbar-search pull-left" action="">
                <input type="text" data-provide="typeahead" class="typeahead search-query span2" placeholder="Quick Search"/>
              </form>
            </div><!--/.nav-collapse -->
          </div>
        </div>
      </div>
      <div class="container-fluid push-bottom">
        <div id="banner">
          <a href="http://agu.org"><img src="http://sites.agu.org/wp-content/themes/agu/images/layout/banner.jpg" alt="AGU - Earth | Oceans | Atmosphere | Space | Planets" title="AGU - Earth | Oceans | Atmosphere | Space | Planets" hspace="0" vspace="0" border="0" align="top" usemap="#Map"></a>
        </div>
        <h2>Abstract Browser Issue Report</h2>
<?php

$inputs = array(); 
$inputs["name"] = (array_key_exists("name",$_POST) && $_POST["name"] != "") ? substr($_POST["name"],0,100) : null;
$inputs["email"] = (array_key_exists("email",$_POST) && $_POST["email"] != "") ? substr($_POST["email"],0,100) : null;
$inputs["description"] = (array_key_exists("description",$_POST) && $_POST["description"] != "") ? substr($_POST["description"],0,1000) : null;
$inputs["type"] = (array_key_exists("type",$_POST) && $_POST["type"] != "") ? substr($_POST["type"],0,100) : null;
$inputs["priority"] = (array_key_exists("priority",$_POST) && $_POST["priority"] != "") ? substr($_POST["priority"],0,100) : null;
$inputs["url"] = (array_key_exists("url",$_REQUEST) && $_REQUEST["url"] != "") ? substr($_REQUEST["url"],0,1000) : null;
$inputs["first"] = (array_key_exists("first",$_REQUEST) && $_REQUEST["first"] != "") ? substr($_REQUEST["first"],0,1) : null;
$inputs["admin"] = (array_key_exists("admin",$_REQUEST) && $_REQUEST["admin"] != "") ? substr($_REQUEST["admin"],0,1) : null;

$priority_options = array("major" => "Major","minor" => "Minor");
$type_options = array("data" => "Data Issue", "behavior" => "Behavior Issue", "aesthetic" => "Aesthetic Issue");

function get_input($inputs,$name) {
  $value = ($inputs[$name] != null) ? "value=\"" . $inputs[$name] . "\" " : "";
  return "<input type=\"text\" name=\"$name\" $value/>";
}

function get_selector($inputs,$name,$options) {
  $select = "<select name=\"$name\">";
  foreach ($options as $key => $value) {
    $selected = ($inputs[$name] == $key) ? "selected" : "";
    $select .= "<option value=\"$key\" $selected>$value</option>";
  }
  return $select . "</select>";
}

function get_issue_form($inputs) {
  global $priority_options, $type_options;
  $description = ($inputs["description"] != null) ? $inputs["description"] : "";
  $form = "<form method=\"POST\" action=\"issue.php\"><table>" .
    "<tr><td><b>Name: </b></td><td>" . get_input($inputs,"name") . "</td></tr>" .
    "<tr><td><b>Email: </b></td><td>" . get_input($inputs,"email") . "</td></tr>" .
    "<tr><td><b>URL: </b></td><td>" . get_input($inputs,"url") . "</td></tr>" .
    "<tr><td><b>Type: </b></td><td>" . get_selector($inputs,"type",$type_options) . "</td></tr>" .
    "<tr><td><b>Priority: </b></td><td>" . get_selector($inputs,"priority",$priority_options) . "</td></tr>" .
    "<tr><td><b>Description: </b></td><td><textarea rows=\"4\" name=\"description\">$description</textarea></td></tr>" .
    "<tr><td></td><td><input style=\"float:right\" type=\"submit\" /></td></tr>" .
    "</table></form>";
  return $form;
}

function get_error_msg($inputs) {
  $missing = array();
  if ($inputs["description"] == null) $missing[] = "Description";
  if ($inputs["email"] == null) $missing[] = "Email";
  if ($inputs["url"] == null) $missing[] = "URL";
  if ($inputs["first"] == null && count($missing) > 0) 
    return "<p style=\"color:red\">Must provide input for: " . implode(", ",$missing) . "</p>";
  else return "";
}

class IssueDB extends SQLite3
{
    function __construct()
    {
        $this->open('sqlite/issues');
    }
}

function create_issue_table($db) {
  $query = 'CREATE TABLE issues ( ' .
    'name varchar(255), ' .
    'email varchar(255), ' .
    'url varchar(255), ' .
    'type varchar(255), ' .
    'priority varchar(255), ' .
    'description varchar(1023), ' .
    'status int )';
  return $db->exec($query);
}

if ($inputs["admin"] != null) {
  $db = new IssueDB();
  if ($db) {
    $result = $db->query("SELECT * FROM issues");
    if ($result == null) {
      echo "<p>No issues in the database.</p>";
    }
    while ($row = $result->fetchArray()) {
       var_dump($row);
    }
  } else {
    echo "<p>Cannot access admin interface right now, please try again later.</p>";
  }
}

//Process issue report and link back to page
else if ($inputs["email"] != null && $inputs["description"] != null && $inputs["url"] != null) {
  $db = new IssueDB();
  if ($db) {
    $values = implode("','",array($inputs["name"],$inputs["email"],$inputs["url"],$inputs["type"],$inputs["priority"],$inputs["description"]));
    $values = "'" . $values . "',0";
    $success = $db->exec("INSERT INTO issues VALUES ($values)");
    echo "<p>Report submitted successfully.</p>";
    echo "<p><a href=\"" . $inputs["url"] . "\">Go back to browsing.</a></p>";
  } else {
    echo "<p>Error processing report, please try again later.</p>";
    echo "<p><a href=\"" . $inputs["url"] . "\">Go back to browsing.</a></p>";
  }
  //$fp = fopen("/var/log/abstract-reports.log","a");
  //fputcsv($fp,array($inputs["url"],$inputs["description"],$inputs["priority"],$inputs["type"],$inputs["email"],$inputs["name"]));
}

//Provide issue report form
else {
  echo get_error_msg($inputs);
  echo get_issue_form($inputs);
}

?>
      </div>
      <div class="push"><!--//--></div>
    </div>
    <footer class="navbar-inner">
      <span>Created by <a href="http://tw.rpi.edu/web/person/EricRozell">Eric Rozell</a> and <a href="http://narock.github.io">Tom Narock</a>. Powered by <a href="http://lodspeakr.org/">LODSPeaKr</a>.</span>
    </footer>
  </body>
</html>
