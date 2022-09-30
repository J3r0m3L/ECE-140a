console.log("File Connected");

function height_range(height, age) {
    photo_id = height.concat(age);
    let theURL='/photos/'+photo_id;
    console.log("Contacting Server (Height)" + theURL);
    fetch(theURL)
        .then(response=>response.json())
        .then(function(response) {
            //let obj = JSON.parse(response);
            let img = document.getElementById('image')
            img.src = response['name'];
            document.getElementById('owner').innerHTML = response['owner'];
        })
}

function age_range(height, age) {
    photo_id = height.concat(age);
    let theURL='/photos/'+photo_id;
    console.log("Contacting Server (Height)" + theURL);
    fetch(theURL)
        .then(response=>response.json())
        .then(function(response) {
            //let obj = JSON.parse(response);
            let img = document.getElementById('image')
            img.src = response['name'];
            document.getElementById('owner').innerHTML = response['owner'];
        })
}

function both() {
    let height = document.getElementById("height").value;
    let age = document.getElementById("age").value;
    if (height != "NA-NA-") {
        height_range(height, age);
    } else if (age != "NA-NA") {
        age_range(height, age);
    }

}