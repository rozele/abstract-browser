<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>AGU Abstract Browser</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="robots" content="noindex, nofollow" />
    <link href="{{lodspk.home}}css/bootstrap.min.css" rel="stylesheet" type="text/css" media="screen" />
    <link rel="alternate" type="application/rdf+xml" title="RDF/XML Version" href="{{lodspk.local.value}}.rdf" />
    <link rel="alternate" type="text/turtle" title="Turtle Version" href="{{lodspk.local.value}}.ttl" />
    <link rel="alternate" type="text/plain" title="N-Triples Version" href="{{lodspk.local.value}}.nt" />
    <link rel="alternate" type="application/json" title="RDFJSON Version" href="{{lodspk.local.value}}.json" />
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
        .dropdown-menu {
            float:right;
            max-width:40em;
        }
        #busy {
            position:fixed;
            top:50%;
            left:50%;
        }
      	#busy-holder {
	    height:100%;
	    width:100%;
	    position:fixed;
	    left:0;
	    top:0;
	    display: none;
            background-color: black;
	    filter: alpha(opacity=50);
	    filter: progid:DXImageTransform.Microsoft.Alpha(opacity=50);
	    opacity:0.5;
	    -moz-opacity: 0.50;
	    z-index: 1000;
	}
    </style>
    <link href="{{lodspk.home}}css/bootstrap-responsive.min.css" rel="stylesheet" type="text/css" media="screen" />

    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-116892593-1"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'UA-116892593-1');
    </script>

    <script type="text/javascript" src="{{lodspk.home}}js/jquery.js"></script>
    <script type="text/javascript" src="{{lodspk.home}}js/bootstrap.min.js"></script>
    <script type="text/javascript" src="{{lodspk.home}}js/bootstrap-typeahead.js"></script>
    <script type="text/javascript">
    function bifConvert(query) {
      query = query.trim();
      if (query[0] == '"' && query[query.length - 1] == '"') {
        return query;
      }
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
        /*$('.typeahead').typeahead({
            source: function (typeahead, query) {
              $('.typeahead').addClass('wait');[]
              
              return $.get('{{lodspk.home}}search/'+bifConvert(query), { }, function (data) {
                  $('.typeahead').removeClass('wait');[]
                  return typeahead.process(data);
              }, 'json');
            },
            onselect: function (obj) {
              $('.typeahead').attr('disabled', true);
              window.location = obj.uri;
            },
            matcher: function (obj) {
              return 1;
            }
        });*/
        $('.report').attr('href',$('.report').attr('href') + '?first=true&url=' + escape(window.location));
        $('a:not(".busyignore"').click(function(evt) {
          $('#busy-holder').show();
	});
    });
    </script>
  </head>
  <body>
    <div id="busy-holder" style="display: none">
      <div id="busy"><img src="{{lodspk.home}}images/loading.gif" width="66px" /></div>
    </div>
    <div class="wrapper">
      <div class="navbar">
        <div class="navbar-inner">
          <div class="container">
            <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
            </a>
            <a class="brand" href="{{lodspk.home}}"><span>{{lodspk.title|urldecode}}</span></a>
            <div class="nav-collapse">
              <ul class="nav">
                <li><a href="{{lodspk.home}}">About</a></li>
                <!--<li><a href="{{lodspk.home}}classes">Classes</a></li>-->
                <!--<li><a href="{{lodspk.home}}namedGraphs">Named Graphs</a></li>-->
                <li><a href="{{lodspk.home}}meetings">Meetings</a></li>
                <li><a href="{{lodspk.home}}vps">Virtual Posters</a></li>
                <!--<li><a href="{{lodspk.home}}people">Authors</a></li>-->
                <li><a href="{{lodspk.home}}sections">Sections</a></li>
                <li><a href="{{lodspk.home}}keywords">Index Terms</a></li>
                <!--<li><a href="{{lodspk.home}}dbsearch.php">Advanced Search</a></li>-->
              </ul>
              <form class="navbar-search pull-left" action="{{lodspk.home}}dbsearch.php">
                <input type="text" data-provide="typeahead" name="q[]" class="typeahead search-query span2" placeholder="Quick Search"/>
                <input type="hidden" name="field[]" value="all"/>
                <input class="btn" type="submit"/>
              </form>
            </div><!--/.nav-collapse -->
          </div>
        </div>
      </div>
      <div class="container-fluid">
