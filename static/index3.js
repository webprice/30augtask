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
        trHTML += '<td><img width="150px" src="'+object['photo']+'" class="avatar" /></td>';
        trHTML += '<td>'+object['seller']+'</td>';
        trHTML += '<td><button type="button" class="btn btn-outline-danger" onclick="userDelete('+object['id']+')">Del</button></td>';
        trHTML += "</tr>";
      }
      document.getElementById("mytable").innerHTML = trHTML;
    }
  };
}

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
        trHTML += '<td><img width="150px" src="'+object['photo']+'" class="avatar" /></td>';
        trHTML += '<td>'+object['seller']+'</td>';
        trHTML += '<td><button type="button" class="btn btn-outline-danger" onclick="userDelete('+object['id']+')">Del</button></td>';
        trHTML += "</tr>";
      }
      document.getElementById("mytable").innerHTML = trHTML;
    }
  };
}

function userDelete(id) {
  const xhttp = new XMLHttpRequest();
  xhttp.open("GET", `${window.location.origin}/test_delete/${id}` );
  xhttp.send();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
      const objects = JSON.parse(this.responseText);
      Swal.fire(`Item ${id} has been removed from the database`);
      existingData();
    }
  };
}






