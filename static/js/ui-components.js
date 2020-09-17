function registerUser()
{
    var first_name = document.querySelectorAll("input")[1].value;
    var last_name = document.querySelectorAll("input")[2].value;
    var phone_number = document.querySelectorAll("input")[3].value;
    var email = document.querySelectorAll("input")[4].value;
    var first_pwd = document.querySelectorAll("input")[5].value;
    var second_pwd = document.querySelectorAll("input")[6].value;
    var birthday = document.querySelectorAll("input")[7].value;
    var country = document.getElementById("country");
    country = country[country.selectedIndex].value;

    if(first_name == "")
    {
        alert("First name can not be empty.");
        return;
    }
    if(last_name == "")
    {
        alert("Last name can not be empty.");
        return;
    }
    if(phone_number == "")
    {
        alert("Phone number can not be empty.");
        return;
    }
    if(email == "")
    {
        alert("Email can not be empty.");
        return;
    }
    if(first_pwd == "")
    {
        alert("first password can not be empty.");
        return;
    }
    if(second_pwd == "")
    {
        alert("Second password can not be empty.");
        return;
    }
    if(birthday == "")
    {
        alert("Birth date can not be empty.");
        return;
    }

    if(first_pwd != second_pwd)
    {
        alert("Please enter same password.");
        return;
    }

    var postdata = {}
    postdata['first_name'] = first_name;
    postdata['last_name'] = last_name;
    postdata['phone_number'] = phone_number;
    postdata['email'] = email;
    postdata['pwd'] = first_pwd;
    postdata['birthday'] = birthday;
    postdata['country'] = country;

    var url = "http://127.0.0.1:8000/registration/";
    var xhttp = new XMLHttpRequest();
    var csrftoken = getCookie('csrftoken');
    xhttp.open("POST", url, false);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.onreadystatechange  = function() {
        if(this.status != 200)
        {
            alert("email address or phone number is not correct.")
            return;
        }
        else{
            window.location = '/index';
        }
    };
    xhttp.send(JSON.stringify(postdata));


}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function login()
{
    var email = document.querySelectorAll("input")[1].value;
    var pwd = document.querySelectorAll("input")[2].value;

    if(email == "" || pwd == "")
    {
        alert("email or password can not be empty.");
    }

    var postdata = {}
    postdata['email'] = email;
    postdata['pwd'] = pwd;

    var url = "http://127.0.0.1:8000/login/";
    var xhttp = new XMLHttpRequest();
    var csrftoken = getCookie('csrftoken');
    xhttp.open("POST", url, false);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.onreadystatechange  = function() {
        if(this.status != 200)
        {
            alert("username or password is not correct.")
            return;
        }
        else {
            window.location = '/index';
        }
    };

    xhttp.send(JSON.stringify(postdata));

}