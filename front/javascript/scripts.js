/*
  ---------------------------------------------------------------------------------------------------
  Function to retrieve the list of equipment monitoring data from from the database server by GET 
  request and show in a HTML table displayed to the user.
  ---------------------------------------------------------------------------------------------------
*/

const getListShow = async () => {
  let url = 'http://127.0.0.1:5000//equipments_monitoring';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.EquipmentsMonitoring.forEach(equipment => insertList(equipment.type, 
                                                        equipment.tag, 
                                                        equipment.temperature,
                                                        equipment.pressure, 
                                                        equipment.vibration, 
                                                        equipment.humidity, 
                                                        equipment.outcome))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Function to clear the table before load the data.
  --------------------------------------------------------------------------------------
*/
const clearTable = () => {
  var table = document.getElementById('dataTable');
  // Remove all the rows except the first one
  while(table.rows.length > 1) {
    table.deleteRow(1);
  }
}

/*
  --------------------------------------------------------------------------------------
  Função to reload the list from the server.
  --------------------------------------------------------------------------------------
*/
const refreshList = async () => {
  clearTable();
  await getListShow();
}

/*
  ---------------------------------------------------------------------------------------------------
  Function call to load the initial data from the database server when the application starts.
  ---------------------------------------------------------------------------------------------------
*/
document.addEventListener('DOMContentLoaded', function() {
  getListShow();
});


/*
  ---------------------------------------------------------------------------------------------------
  Function to get new equipment monitoring data, predict diagnosis and send to the database server 
  using a POST request.
  ---------------------------------------------------------------------------------------------------
*/
const postEquipmentMonitoring = async (inputType, inputTag, inputTemperature, inputPressure, 
  inputVibration,inputHumidity) => {
  const formData = new FormData();

  // Append all input values to the FormData object.
  formData.append('type', inputType);
  formData.append('tag', inputTag);
  formData.append('temperature', inputTemperature);
  formData.append('pressure', inputPressure);
  formData.append('vibration', inputVibration);
  formData.append('humidity', inputHumidity);


  let url = 'http://127.0.0.1:5000/equipment_monitoring';
  // Send the POST request to the server with the form data.
  return fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .then((data) => {
      return data; // Return equipment data with diagnosis
    })
    .catch((error) => {
      console.error('Error:', error);
      throw error;
    });
}



/*
  ---------------------------------------------------------------------------------------------------
  Function to create a close button for each item in the list
  ---------------------------------------------------------------------------------------------------
*/
const insertButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7"); // Unicode for the "×" character.
  span.className = "close"; // Add a class for styling the button.
  span.appendChild(txt); // Attach the "×" text to the button.
  parent.appendChild(span); // Add the button to the parent element.
}



/*
  ---------------------------------------------------------------------------------------------------
  Function to delete an equipment monitoring from the list when the "close" button is clicked.
  ---------------------------------------------------------------------------------------------------
*/
const removeElement = () => {
  let close = document.getElementsByClassName("close");

  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement; // Get the parent element of the button.
      const typeEquipment = div.getElementsByTagName('td')[0].innerHTML // Retrieve the type value.
      const tagEquipment = div.getElementsByTagName('td')[1].innerHTML // Retrieve the tag value.
      
      // Confirm deletion with the user.
      if (confirm("Are you sure?")) {
        deleteEquipMonitoring(typeEquipment,tagEquipment) // Call the function to delete the item from the server.
        div.remove() // Remove the element from the DOM.
        alert("Deleted!")
      }
    }
  }
}


/*
  ---------------------------------------------------------------------------------------------------
  Function to delete an equipment monitoring data from the server using a DELETE request.
  ---------------------------------------------------------------------------------------------------
*/
const deleteEquipMonitoring = (type,tag) => {

  // Log the type and tag value for debugging.
  let url = `http://127.0.0.1:5000/equipment_monitoring?type=${type}&tag=${tag}`;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  ---------------------------------------------------------------------------------------------------
  Function to add a new equipment monitoring data to the list and the database server.
  ---------------------------------------------------------------------------------------------------
*/


const newEquipmentMonitoring = () => {
  event.preventDefault();
  let inputType = document.getElementById("newType").value.toUpperCase();
  let inputTag = document.getElementById("newTag").value.toUpperCase();
  let inputTemperature = document.getElementById("newTemperature").value.toUpperCase();
  let inputPressure = document.getElementById("newPressure").value.toUpperCase();
  let inputVibration = document.getElementById("newVibration").value.toUpperCase();
  let inputHumidity = document.getElementById("newHumidity").value.toUpperCase();

  // check if the equipment exist before adding on the list - check by primary key
  const checkUrl = `http://127.0.0.1:5000/equipment_monitoring?type=${inputType}&tag=${inputTag}`;
  fetch(checkUrl, {
    method: 'get'
  })
    .then((response) => response.json())
    .then(async (data) => {
      // Validate user input before proceeding.
      if (data.equipments && data.equipments.some(equipment => equipment.type === inputType 
        && equipment.tag === inputTag)) {
        alert("The pair Tag and Project already exists in the database!")
      } else if (inputType === '') {
      alert("Write the Equipment type!");
      } else if (inputTag === ''){
      alert("Write the Tag number!");
      } else if (! isNaN(+inputType) || 
      ! isNaN(+inputTag)) {
        alert("Type and Tag most not be numbers!");
      } else if (isNaN(inputTemperature) || isNaN(inputPressure) || 
      isNaN(inputVibration) || isNaN(inputHumidity) ) {
      alert("Temperature, Pressure, Vibration Amplitude and Humidity must be numbers!");
      } else {
        try {
          // Send data to the server and wait for the diagnostic
          postEquipmentMonitoring(inputType, inputTag, inputTemperature, inputPressure, inputVibration, 
        inputHumidity) 
        .then( result => {
            // Clean the form
          document.getElementById("newType").value = "";
          document.getElementById("newTag").value = "";
          document.getElementById("newTemperature").value = "";
          document.getElementById("newPressure").value = "";
          document.getElementById("newVibration").value = "";
          document.getElementById("newHumidity").value = "";

          // Reload equipment monitoring list to show new equipment with diagnosis
          refreshList();
          
          
          // Show the prediction result
          const diagnosis = result.outcome === 1 ? "FAULTY" : "NOT FAULTY";
          alert(`Equipment monitoring data added sucessfuly!\nDiagnosis: ${diagnosis}`);
          
          // Scroll the sheet to show new result
          document.querySelector('.equipmentsMonitoring').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
          });
          // return result
        })
          .catch ((error) => {
          console.error('Error to add new equipment monitoring data:', error);
          alert("Error to add new equipment monitoring data. Try again!");
        });
        } catch (error) {
          console.error('Error to add new equipment monitoring data:', error);
          alert("Error to add new equipment monitoring data. Try again!");
        }
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      alert("Error to check for equipment monitoring data. Try again!");
    });
}



/*
  ---------------------------------------------------------------------------------------------------
  Function to insert a new equipment monitoring data into the HTML table displayed to the user.
  ---------------------------------------------------------------------------------------------------
*/
const insertList = (type, tag, temperature, pressure, vibration, humidity, outcome) => {
  
  let equipment_monitoring = [type, tag, temperature, pressure, vibration, humidity]

  let table = document.getElementById('dataTable');
  let row = table.insertRow(); // Create a new row in the table.

  // Add each value to a cell in the row.
  for (let i = 0; i < equipment_monitoring.length; i++) {
    let cel = row.insertCell(i);
    cel.textContent = equipment_monitoring[i];
  }

  // Insert diagnostic cell in the table sheet
  var diagnosticCell = row.insertCell(equipment_monitoring.length);
  const diagnosticText = outcome === 1 ? "FAULTY" : "NOT FAULTY";
  diagnosticCell.textContent = diagnosticText;
  
  // Aplpply styling based on diagnosis result 
  if (outcome === 1) {
    diagnosticCell.className = "Faulty";
  } else {
    diagnosticCell.className = "Not faulty";
  }

  // Insert delete button
  var deleteCell = row.insertCell(-1);
  insertDeleteButton(deleteCell);

  removeElement();
}

/*
  --------------------------------------------------------------------------------------
  Funçction to create a close button to each equipment monitoring data in the list
  --------------------------------------------------------------------------------------
*/
const insertDeleteButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}


