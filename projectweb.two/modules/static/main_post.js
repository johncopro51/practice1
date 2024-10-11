




// to show commenting field
function show_comment(){
  $("#show_comment").toggleClass("dissapear"); 

}
// To submit form with an input or <a>
function submit_form(val)
{
document.getElementById(val).submit(); 
}


// showing reply field
function show_reply_field(val){
document.getElementById('replyfield'+val).classList.toggle("dissapear"); 
}

function refresh_box(value) {
  $("."+value).toggleClass("dissapear"); 

}

