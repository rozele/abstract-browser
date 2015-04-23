<script type="text/javascript">
//<![CDATA[
  $(document).ready(function() {
    $("#keywordHome").find("#keywordSearch").change(function(e) {
      var pref = (window.location.pathname.match(".*search/$")) ? "" : "search/" ;
      $("#keywordHome").find("#keywordSubmit").attr("href", pref + jQuery(e.target).val());
    });
  });
//]]>
</script>