
//
// Add job:
// if used with no args, add job with mkdir operation at the last.
//
addjob = function(sortofop, id, time, iffail, numofoperations){
 var jobtemplate=$("#jobtemplate").html()

 if (!sortofop) {
  sortofop=$("#sortofop").val();
 }
 if (sortofop == "dummy") {
   return 0; // do nothing;
 }

 var numofelements=$("#jobformdata").children().length + 1;

 $("#jobformdata").append(jobtemplate);
 bind_deljobwhenclicked();
 lastelement=$("#jobformdata").children().last()

 if (!numofoperations){
  numofoperations=1;
 }
 for (i=0; i < numofoperations; i++){
  addoperation(sortofop, lastelement);
 }

 if (!id){
  id=numofelements;
 }
 if (!iffail){
  iffail="stop";
 }

 // set form values:
 $("[name=id]").last().val( id )
 $("[name=time]").last().val( time )
 $("[name=iffail]").last().val( iffail )


 resetjobnumber();

}

//
addoperation = function(sortofop, lastelement){
 var operationtemplate=$("#"+sortofop+"template").html()
 lastelement.append(operationtemplate);
}

deljob = function(){
 delpos1=$("#delpos1").val();
 if (!delpos1){
  $("#jobformdata .job").last().remove();
 }
 else {
  $("#jobformdata .job").eq(delpos1 - 1).remove();
 }
 resetjobnumber();
}


changejobpos = function(){
  jobpos1=$("#jobpos1").val();
  jobpos2=$("#jobpos2").val();
  srcdiv=$(".job").eq(jobpos1);
  $(".job").eq(jobpos2).after(srcdiv)

 resetjobnumber();
}

resetjobnumber = function() {
 $(".jobnumber").each( function(index){
   $(this).text(index + " ");
  }
 );
}

bind_deljobwhenclicked = function(){
 $(document).on("click", ".jobdelbutton",
  function(event){
    $(this).parent().remove();
    resetjobnumber();
  }
 )
}

binddupdeltooperation = function(op){
 $(document).on("click", "."+op+"start",
  function(event){
   if (event.ctrlKey){
    $(this).parent().remove();
   }
   else {
    // firstly, add operation component:
    addoperation(op, $(this).parent().parent());
    // then duplicate values:
    var tmparray=[];
    $(this).parent().children().each( 
     function(){
      tmparray.push($(this).val())
     }
    )
    // add them to next element:
    $(this).parent().nextAll().last().children().each( 
     function(){
      var tmp=tmparray.shift();
      $(this).val(tmp);
     }
    )
   }
  }
 );
}


// jquery event:
$(document).ready(function(){

 // deal with multiop jobs
 for (var op in multioplist){
  binddupdeltooperation(op);
 }

 // set jquery file upload
 $(function () {
  $('#fileupload').fileupload({
   dataType: 'text',
   done: function (e, data) {
    $('#load_and_reload').prop("value", "reload")
   }
  });
 });

});
