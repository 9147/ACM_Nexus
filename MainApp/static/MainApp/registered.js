function openBlock(){
    document.getElementById('block').style.display='flex';
}
function closeBlock(){
    document.getElementById('block').style.display='none';
}
function validateForm(){
    // alert($('passward').val(),$('passward2').val());
    if(document.getElementById('password').value.length<4){
        alert("passwords must be atleast of 4 characters");
        return false;
    }
    else if(document.getElementById('password').value!==document.getElementById('password2').value){
        alert("passwords don't match");
        return false;
    }

}


