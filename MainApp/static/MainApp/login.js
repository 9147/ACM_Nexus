function login(){
    console.log("login");
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    console.log(email, password);
    var data = {
        email: email,
        password: password,
    };
    console.log(data);

    setRequestHeader();

    $.ajax({
        dataType: 'json',
        type: 'POST',
        url: "/signin/",
        data: data,
        success: function (data) {
            console.log("Success:", data);
            window.location.href = "../";
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(data)
            alert("login failed!! ")

        }
    });

}

function validateForm() {
    var year = document.getElementById("year").value;
    if(year<2024 || year>2028){
    alert("Invalid Year!!\n year should be between 2024 and 2027");
        return false
    }
    return true;
  }