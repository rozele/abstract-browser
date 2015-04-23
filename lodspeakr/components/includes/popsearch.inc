<script type="text/javascript">
//<![CDATA[
  $(document).ready(function() {
    $("#popsearch").find("#search").change(function(e) {
      var pref = "";
      if (!window.location.pathname.match("/$")) {
        pref = (window.location.pathname.match(".*search/.*$"))
          ? window.location.pathname.replace(/search\/.*$/gi,"search/")
          : window.location.pathname + "/search/" ;
      } else {
        pref = "search/" ;
      }
      $("#popsearch").find("#submit").attr("href", pref + jQuery(e.target).val());
      $("#popsearch").find("#searchform").attr("action", pref + jQuery(e.target).val());
    });
  });
//]]>
</script>