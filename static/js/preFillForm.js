
var preFillFormular = function () {
	// + Subroutine to get the parameters from the URL.
	var getParameters = function () {
	  var params = {}; 
	  if (location.search) {
	    var parts = location.search.substring(1).split('&');
	    for (var i = 0; i < parts.length; i++) {
	      var nv = parts[i].split('=');
	      if (!nv[0]) continue;
	      params[nv[0]] = nv[1] || true;
	    }
	    return params
	  }
	  return null;
	};
	// + First Check for Parameters:
	var params = getParameters();
	if(params) {
		// + Select the input fields: 
		var $nodeName = $('input[name="hostname"]')[0],
		  $key = $('input[name="key"]')[0],
		  $mac = $('input[name="mac"]')[0];
		if($nodeName && params.nodename) {
			$nodeName.value = params.nodename;
		}
		if($key && params.key){
			$key.value = params.key;
		}
		if($mac && params.mac){
			$mac.value = params.mac;
		}
		$('#infoFromRouter').removeClass('hidden');
	}
};
