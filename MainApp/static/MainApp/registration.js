function validateForm() {
    var name = document.getElementById("name").value;
    var email1 = document.getElementById("email1").value;
    var email2 = document.getElementById("email2").value;
    var email3 = document.getElementById("email3").value;
    var email4 = document.getElementById("email4").value;
    var problem = document.getElementById("problem").value;

    if (email1 == email2 || email1 == email3 || email1 == email4 || email2 == email3 || email2 == email4 || email3 == email4) {
        alert("Duplicate Email's found!! Team Creation Failed");
        return false;
    } else if (problem < 1 || problem > 25) {
        alert("Invalid Problem Number!! Team Creation Failed");
        return false;
    }

    console.log(problem, typeof (problem));
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
            'problem': problem,
        },
        dataType: 'json',
        success: function (data) {
            console.log(data);
            // Submit the form programmatically after successful AJAX call
            document.getElementById("form").submit();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(errorThrown);
            alert(errorThrown + "!! Team Creation Failed");
            // Handle error, no form submission
        }
    });

    return false; // Prevent default form submission
}