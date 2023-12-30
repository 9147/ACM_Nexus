function validateForm(){
    var name = document.getElementById("name").value;
    var email1 = document.getElementById("email1").value;
    var email2 = document.getElementById("email2").value;
    var email3 = document.getElementById("email3").value;
    var email4 = document.getElementById("email4").value;
    if(email1 == email2 || email1 == email3 || email1 == email4 || email2 == email3 || email2 == email4 || email3 == email4){
        alert("Duplicate Email's  found!! \n Team Creation Failed");
        return false;
    }
    setRequestHeader();

    $.ajax({
        url: '/checkteam/',
        type: 'POST',
        data: {
            'name': name,
            'email1': email1,
            'email2': email2,
            'email3': email3,
            'email4': email4,
        },
        dataType: 'json',
        success: function (data) {
            console.log(data);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(errorThrown);
            alert(errorThrown+"!!\n Team Creation Failed")
            // return false;
            window.location.href = "../registration/";
        }
    });
    return true;
}