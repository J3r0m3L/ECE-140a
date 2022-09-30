var object = 0;

function enter() {
    object = document.getElementById("input").value;
    let gps = document.getElementById("coordinates");

    theURL1 = '/find_object/' + object
    theURL2 = '/pid_tracking/' + object
    console.log("Enter Called")
    
    fetch(theURL1)
        .then((response) => response.json())
        .then(function(response) {
            console.log("theURL1")
            document.getElementById('coordinates').innerHTML = response;
            console.log(typeof(response))
            console.log("Object found")
          
        });
        
   
    fetch(theURL2)
        .then((response) => response.json())
        .then(function(response) {
            console.log("broken")
    
        });
}   
  
function coords() {
    let gps = document.getElementById("coordinates").innerHTML;
    gps = gps.split(' ').join('')
    gps = gps.split(',').join('')
    theURL = '/store_coords/' + object + gps;
    fetch(theURL)
            .then((response) => response.json())
            .then(function(response) {
                console.log("response stored")
            });
}
