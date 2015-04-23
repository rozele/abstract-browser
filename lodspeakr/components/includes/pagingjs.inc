<script type="text/javascript">
  function refreshPaging(count,term) {
    $('#busy-holder').show();
    if (document.location.href.match(new RegExp(term+"[\\/\\d]*(#.*)?$","gi")) != null) {
      window.location = document.location.href.replace(new RegExp(term+"[\\/\\d]*(#.*)?$","gi"), term+"/"+count+RegExp.$1);
    } 
    else if (document.location.href.match(/\.html$/gi) != null) {
      window.location = document.location.href.replace(/\.html$/gi,"/"+term+"/"+count);
    }
    else {
      window.location = document.location.href + count;
    }
  }
  
  function setSelectValue(el, val) {
    $(el).find("option[value="+val+"]").attr("selected","selected");
  }

  $("#limitsel").find("option").removeAttr("selected");
  $("#limitsel").find("option[value={{limit}}]").attr("selected","selected");
</script>