function select_sensor() {
  let the_sensor = document.getElementById("sensor").value;
  return the_sensor;
}

function select_distance() {
  let the_distance = document.getElementById("distance").value;
  return the_distance;
}

function select_voltage() {
  let the_voltage = document.getElementById("voltage").value;
  return the_voltage;
}

function buzzing() {
  let theURL = "/buzzer";
  fetch(theURL)
  console.log("Buzzing")
}

function submit() {
  let selected_name = select_sensor();
  console.log(selected_name);
  let distance_range = select_distance();
  console.log(distance_range);
  let voltage_range = select_voltage();
  console.log(voltage_range);

  let theURL =
    "/name/" + selected_name + "/distance/" + distance_range + "/voltage/" + voltage_range;
  console.log(theURL);
  console.log("Starting executing range");
  fetch(theURL)
    .then((response) => response.json())
    .then(function (response) {
      for (var key in response) {
        let container = document.getElementById("all_values")

        let item1 = document.createElement("p");
        let item2 = document.createElement("p");
        let item3 = document.createElement("p");
        let item4 = document.createElement("p");
        
        item1.innerText = "id: " + response[key]["id"];
        item2.innerText = "sensor:" + response[key]["sensor"];
        item3.innerText = "distance: " + response[key]["distance"];
        item4.innerText = "voltage: " + response[key]["voltage"];

        container.appendChild(item1)
        container.appendChild(item2)
        container.appendChild(item3)
        container.appendChild(item4)
      }
    });
}
