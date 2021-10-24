
function submission(s) {
    window.location.reload();

    let dist_response = document.getElementById('distance').value;
    if (dist_response == '') {
        dist_response = 5; // default radius
    }
    let limit_response = document.getElementById('limit').value;
    if (limit_response == ''){
        limit_response = 5;
    }
    let is_closed_response = !(document.getElementById('is_closed').checked);
    // is_closed will be false if the checkbox is checked (true) because we will
    // not be showing closed shops.
    
    if (parseInt(dist_response) < 0) {
        // we need to make sure the user enters at least 0
        alert('please input a positive number for the distance');
    } else if (parseInt(limit_response) < 0) {
        // limit is less than zero
        alert('please input a positive number for the amount of stores');
    } else {
        let latitude;
        let longitude;
        window.navigator.geolocation.getCurrentPosition(function (response) {
            latitude = response.coords.latitude;
            longitude = response.coords.longitude;
            console.log(latitude, longitude);

            let data = {
                'latitude': latitude, 
                'longitude': longitude, 
                'distance': dist_response, 
                'is_closed': is_closed_response,
                'limit': limit_response
            }
            console.log(data);
        
            $.ajax({
                type: "POST",
                url: "/",
                data: JSON.stringify(data),
                contentType: 'application/json'
            });
        });
    }


}