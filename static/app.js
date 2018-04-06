window.onload = displayLikes();

window.onload = function() {
    document.getElementById('likeaddbutton').addEventListener('click', formsubmit, false);
}

function makeRequest(){
    // Checks browser compatibility and returns a new HTTP request
    var httpRequest;

    if (window.XMLHttpRequest){
        httpRequest = new XMLHttpRequest(); // Chrome, Mozilla etc.
    }
    else if (window.ActiveXObject){ // Internet Explorer
        try{
            httpRequest  = new ActiveXObject("Msxml2.XMLHTTP");
        }
        catch (e){
            try{
                httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
            }
            catch (e){}
        }
    }
    return httpRequest;
}

function displayLikes(){
    var httpRequest = makeRequest();

    // The following code block will only execute when a response has been obtained
    httpRequest.onreadystatechange = function(){
        // check that state changes have been completed
        if (this.readyState === 4){
            // check that response was 200: OK (can add other status handlers underneath)
            if (this.status === 200){
                var text = "";
                var result = JSON.parse(this.responseText);
                for (i = 0; i < result.likes.length; i++){
                    var thelike = result.likes[i]
                    text += "<input class='mr-2' type='checkbox' name='checks' value='" + thelike + "'>" + thelike + "</input></br>"
                }
                document.getElementById('likeslist').innerHTML = text;
            }
            // Put else if statements for other responses here
        }
    }
    httpRequest.open('GET', '/likes')
    httpRequest.send(null) // Not passing any data as its a get req.
}

function formsubmit(){

    var httpRequest = makeRequest();

    httpRequest.onreadystatechange = function(){
        if (this.readyState === 4){
            if (this.status === 200){
                displayLikes();
            }
        }
    }

    // Set up the request parameters ---- method is post, handler is /likes
    httpRequest.open('POST', '/likes');
    // get the form data
    list = [document.getElementById('likeinput').value];
    // convert the form data to a JSON string
    data = JSON.stringify({'likes' : list});
    // tell the server the incoming data is JSON through the HTTP header
    httpRequest.setRequestHeader('Content-Type', 'application/json');
    // send the server the JSON data
    httpRequest.send(data);

    // Reset the form entry
    document.getElementById('likeinput').value = "";

    return false;
}
