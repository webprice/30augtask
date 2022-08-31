//loadTable - invoke by clicking on "refresh data" button at the front-end
//it send request to /load_data endpoint, which triggers data scraping from the OLX(see views.py)
//constructing the table out of the response's data
function loadTable() {
  Swal.fire(`Please wait, scraping in progress...`);
  const xhttp = new XMLHttpRequest();
  xhttp.open("GET", `${window.location.origin}/load_data`);
  xhttp.send();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.responseText);
      var trHTML = '';
      const objects = JSON.parse(this.responseText);
      for (let object of objects) {
        trHTML += '<tr>';
        trHTML += '<td>'+object['id']+'</td>';
        trHTML += '<td>'+object['title']+'</td>';
        trHTML += '<td>'+object['price']+'</td>';
        // trHTML += '<td><img width="150px" src="'+object['photo']+'" class="avatar" /></td>';
        // trHTML += '<td>'+object['seller']+'</td>';
        trHTML += '<td><button type="button" class="btn btn-outline-danger" onclick="userDelete('+object['id']+')">Del</button></td>';
        trHTML += "</tr>";
      }
      document.getElementById("mytable").innerHTML = trHTML;
    }
  };
}

//Firing the request to existing_data endpoint, which must provide the data from the DB in JSON format.
//constructing the table out of the response's data
function existingData() {
  const xhttp = new XMLHttpRequest();
  xhttp.open("GET", `${window.location.origin}/existing_data`);
  xhttp.send();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.responseText);
      var trHTML = '';
      const objects = JSON.parse(this.responseText);
      for (let object of objects) {
        trHTML += '<tr>';
        trHTML += '<td>'+object['id']+'</td>';
        trHTML += '<td>'+object['title']+'</td>';
        trHTML += '<td>'+object['price']+'</td>';
        // trHTML += '<td><img width="150px" src="'+object['photo']+'" class="avatar" /></td>';
        // trHTML += '<td>'+object['seller']+'</td>';
        trHTML += '<td><button type="button" class="btn btn-outline-danger" onclick="userDelete('+object['id']+')">Del</button></td>';
        trHTML += "</tr>";
      }
      document.getElementById("mytable").innerHTML = trHTML;
    }
  };
}

//send the request to test_delete endpoint, which triggers removing row from the DB by it's <id> number
//generating the popup message on success
// and invoking the existingData() JS function that construct the table with the data
function userDelete(id) {
  const xhttp = new XMLHttpRequest();
  xhttp.open("GET", `${window.location.origin}/test_delete/${id}` );
  xhttp.send();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
      // const objects = JSON.parse(this.responseText);
      Swal.fire(`Item ${id} has been removed from the database`);
      existingData();
    }
  };
}






