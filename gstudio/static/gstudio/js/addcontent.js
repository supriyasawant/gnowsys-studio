
 $.noConflict();
   var isWikipage=false;
   var editWikipage=false;
   var objid;
   var isSection=false;
   var editSection=false;
   var isSubsection=false;
   var editSubsection=false;
   var isNode=false;
   function subsecsave(objid){
       var org_data = $("#gnoweditor").val();
       var encode_data = encodeURIComponent(org_data);
       var decode_data = decodeURIComponent(encode_data.replace(/\+/g, " "));
       $("#sectionreply"+objid).val(decode_data);
       $("#subsecsubmit"+objid).trigger('click');
       $(".savesubsec1").hide();
       
   }

    
  jQuery(document).ready(function($) {
       $("#addcontent").one("click",function(){
	   isSection=true;
	          $("#addcontent").hide();
	          //$("#save").show();
		  $("#chart").hide();
	    $("#content").css({"width":"300px",})
	         document.getElementById('gnoweditor').style.visibility="visible";
	        $("#gnoweditor").orgitdown(mySettings);
		 var orgtext = $("#gnoweditor").val();

	   });
	$("#save").one("click",function() {
		var org_data = $("#gnoweditor").val();
		document.getElementById("orgpage").value = org_data;
		var encode_data = encodeURIComponent(org_data);
		$('#submitsec').trigger('click');
	    $("#save").hide();
		});

	$("#pagecontent1").one("click",function() {
	    isWikipage=true;
	$("#chart").hide();
	document.getElementById('gnoweditor').style.visibility="visible";
	$("#gnoweditor").orgitdown(mySettings);
	//$("#save1").show();
	$("#pagecontent1").hide();
	     $("#content").css({"width":"300px",})
	    });
        $("#save1").one("click",function() {
	var org_data = $("#gnoweditor").val();
	document.getElementById("orgpage1").value = org_data;
	var encode_data = encodeURIComponent(org_data);
	$('#submitpage').trigger('click');	

	});
      $(".editseccontent").one("click",function(){
          editSection=true;
	 // $(".saveseccontent").show();
	   $("#content img").css({"max-width":"600px",})
	   $("#content").css({"width":"600px",})
	  $("#chart").hide();
	  document.getElementById('gnoweditor').style.visibility="visible";
	  $("#gnoweditor").orgitdown(mySettings);
	  var a = this.name;
	  $("#gnoweditor").val(a);
	  var elmts = document.getElementsByClassName("editval");
	  for (var i = 0; i < elmts.length; i++){
	      elmts[i].setAttribute("value","edited");}
	  var screenTop = $(document).scrollTop();
	  $(".orgitdownContainer").css({
	      "margin-top":screenTop,});
	  $("#newsection1").hide();
	  $(".editseccontent").hide();
	  $(".createsubsection").hide();
	  $("#rating").hide();
	  $(".chkbox").hide();
	  $(".deletesec").hide();
	  $(".tag").hide();
	  $(".tagtext").hide();
	  $(".editpagecontent").hide();
	  $(".editsubsec").hide();
      });
       $(".saveseccontent").one("click",function(){
	   var org_data = $("#gnoweditor").val();
	   var elmts = document.getElementsByClassName("reptext");
	   var encode_data = encodeURIComponent(org_data);
	   var decode_data = decodeURIComponent(encode_data.replace(/\+/g, " "));
	   for (var i = 0; i < elmts.length; i++){
	       elmts[i].setAttribute("value",decode_data);}
	   $(".submitresponse").trigger('click');
	   $(".saveseccontent").hide();
		  
       });

       $(".editsubsec").one("click",function(){
	   editSubsection=true;
	   var each_id=$(this).attr("id");
	   $("#chart").hide();
	   $("#content img").css({"max-width":"600px",})
	   
	   $("#content").css({"width":"600px",})
	   document.getElementById('gnoweditor').style.visibility="visible";
	   $("#gnoweditor").orgitdown(mySettings);
	   var org_data=$("#subsec"+each_id).val();
	   $("#edit"+each_id).val("edited");
	   $("#sectionreply"+each_id).val(org_data);
	   $("#gnoweditor").val(org_data);
	   var screenTop = $(document).scrollTop();
	   $(".orgitdownContainer").css({
	       "margin-top":screenTop,});
	    //$("#save"+each_id).show();
	   objid=each_id;
	   $(".editsubsec").hide();
	   $(".submitsubsec1").hide();
	   $(".tag").hide();
	   $(".tagtext").hide();
	   $(".editpagecontent").hide();
	   $("#newsection1").hide();
	   $(".editseccontent").hide();
	   $(".createsubsection").hide();
	   $("#rating").hide();
	   $(".chkbox").hide();
	   $(".deletesec").hide();
       });
       $(".editpagecontent").one("click",function(){
	    editWikipage=true;
      	    $("#chart").hide();
	    $(".editpagecontent").hide();
      	  //  $(".savepagecontent").show();
 	    $("#content img").css({"max-width":"600px",})
	   
	    $("#content").css({"width":"600px",})
	    document.getElementById('gnoweditor').style.visibility="visible";
	    $("#gnoweditor").orgitdown(mySettings);
            var a = this.name;
	    $("#gnoweditor").val(a);
	    var elmts = document.getElementsByClassName("editval");
	    for (var i = 0; i < elmts.length; i++){
		elmts[i].setAttribute("value","edited");}
	   var screenTop = $(document).scrollTop();
      	    $(".orgitdownContainer").css({
      		"margin-top":screenTop,});
	   $(".tag").hide();
	   $(".tagtext").hide();
	   $("#newsection1").hide();
	   $(".createsubsection").hide();
	   $("#rating").hide();
	   $(".chkbox").hide();
	   $(".deletesec").hide();
	   $(".editseccontent").hide();
	   $(".editsubsec").hide();
	  
		    
       });
       $(".savepagecontent").one("click",function(){
	   var org_data = $("#gnoweditor").val();
	   var elmts = document.getElementsByClassName("reptext");
	   var encode_data = encodeURIComponent(org_data);
	   var decode_data = decodeURIComponent(encode_data.replace(/\+/g, " "));
	   for (var i = 0; i < elmts.length; i++){
	       elmts[i].setAttribute("value",decode_data);}
           $(".pagedit").trigger('click');
	   $(".savepagecontent").hide();
      	  
       });
      $("#editnodecontent").one("click",function(){
	  isNode=true;
      	    $("#chart").hide();
	    $("#content img").css({"max-width":"600px",})
	   
	    $("#content").css({"width":"600px",})
	    document.getElementById('gnoweditor').style.visibility="visible";
	    $("#gnoweditor").orgitdown(mySettings);
            var a = this.name;
	 
	    $("#gnoweditor").val(a);
	   var screenTop = $(document).scrollTop();
      	    $(".orgitdownContainer").css({
      		"margin-top":screenTop,});
	   $("#editnodecontent").hide();
	   //$("#savenodecontent").show();
           $("#nodedit").hide();
		    
       });
       $("#savenodecontent").one("click",function(){
	   var org_data = $("#gnoweditor").val();
	   var encode_data = encodeURIComponent(org_data);
	  
	   var decode_data = decodeURIComponent(encode_data.replace(/\+/g, " "));
	   $("#reptext").val(decode_data);
	   $("#nodedit").trigger('click');
	   $("#nodedit").hide();
	   
       });

       $(".createsubsection").one("click",function(){
	           isSubsection=true;
	           //$(".savesubsec").show();
	           //$(".submitsubsec").show();
	           $(".createsubsection").hide();

	           $("#content img").css({"max-width":"600px",})
	           $("#content").css({"width":"600px",})   
		    $("#chart").hide();
		    document.getElementById('gnoweditor').style.visibility="visible";
		    $("#gnoweditor").orgitdown(mySettings);
		    $("#gnoweditor").val('');
		    var screenTop = $(document).scrollTop();
		    $(".orgitdownContainer").css({
			    "margin-top":screenTop,});
		  
	   });
       $(".savesubsec").one("click",function() {
	   var org_data = $("#gnoweditor").val();
	   var elmts = document.getElementsByClassName("reptext");
	   var encode_data = encodeURIComponent(org_data);
	   var decode_data = decodeURIComponent(encode_data.replace(/\+/g, " "));
	   for (var i = 0; i < elmts.length; i++){
	       elmts[i].setAttribute("value",decode_data);}
	   $(".savesubsec").hide();
	   $(".submitsubsec").trigger('click');
       });

      $("#savecontent").one("click",function() {
	      var org_data = $("#gnoweditor").val();
	      var id =  document.getElementById("objectid").value
	       document.getElementById("orgcontent").value = org_data;
	      var encode_data = encodeURIComponent(org_data);
          $("#savecontent").hide();
		         $.ajax({
			       url: '/nodetypes/ajax/contentorgadd/?id=' + id + '&contentorg=' + encode_data,
			       success: function(data) {
			         $.ajax({
				    url: '/nodetypes/ajax/ajaxcreatefile/?id=' +id+ '&content_org=' +encode_data,
				    success: function(data) {
				    	$.ajax({
				    		url: '/nodetypes/ajax/ajaxcreatehtml/',
				    		success: function(data) {
				    		    $.ajax({
				    			    url: '/nodetypes/ajax/contentadd/?id=' +id,
                                                            success: function(data) {
								// alert("Data Saved");
                                                              location.reload();}
				    			});
				    		}      
				     	    });
				     }
				}); 
			    
			       }
			 });
		    
      });

  });
       
    