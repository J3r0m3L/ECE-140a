console.log("File is Connected")

function displayed() {
    let photo_id = document.getElementById('textInput').value;
    document.getElementById('price').innerHTML = "";
    let theURL='/photos/'+photo_id;
    console.log("Making a RESTful request to the server! (Photo)")
    fetch(theURL)
        .then(response=>response.json()) // Convert response to JSON
        .then(function(response) {
            let img = document.getElementById('image') 
            img.src = response['img_src']
        });
}

function priced() {
    let photo_id = document.getElementById('textInput').value;
    let theURL='/prices/'+photo_id;
    console.log("Making a RESTful request to the server! (Price)")
    fetch(theURL)
        .then(function(response) {
            return response.text().then(function(text) {
                document.getElementById('price').innerHTML = '$' + text;
                
            });
        });
    document.getElementById('image').src = ""
}
