function display_results() {
    let photo_id = document.getElementById('input').value;
    let theURL = '/photos/' + photo_id;
    console.log(theURL)

    console.log("Requesting Server for Image Source")
    fetch(theURL).then(response => response.json())
        .then(function(response) {
            document.getElementById('license_image').src = './images/' + response['img_src']
        });

    theURL = '/text/' + photo_id
    console.log(theURL)
    console.log("Requesting Server for Image Text")
    let d = new Date();

    console.log(d.getMilliseconds());
    fetch(theURL).then(response => response.json())
        .then(function(response) {
            document.getElementById('text_read').innerHTML = "text detected: " + response[0];
            document.getElementById('cropped_image').src = "./images/Result.png?random=" + String(d.getMilliseconds());

        })
}