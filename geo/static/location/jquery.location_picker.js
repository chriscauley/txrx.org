// loosny based off of http://www.randomsequence.com/articles/django-admin-google-maps-location-picker-with-jquery/
google.load("maps", "3",{"other_params": "sensor=true"});

$(document).unload(function(){
    GUnload();
});

function loadAddress(that) {
    var form = $(that).closest(".inline-group,.module");
    var address = form.find("[name=address]").val();
    var city = form.find("[name=city]");
    var cities = form.find("[name=city]").children();
    for (i=0; i<cities.length; i++) {
	if (city.val()==cities[i].value){ city = cities.eq(i).text(); }
    }
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({address:address+", "+city},function(results){
	setLocation(results[0].geometry.location);
    });
}

function setLocation(location) {
    var that = $("input.location_picker")[0];
    var lat = location.lat(), lon = location.lng();
    that.value = lat+','+lon;
    if (that.marker != null) { that.marker.setMap(null); }
    that.marker = new google.maps.Marker({position:location,map:map,title:$("#id_name").val()});
    //document.getElementById("id_lat").value = (lat+'').slice(0,10);
    //document.getElementById("id_lon").value = (lon+'').slice(0,10);
}

$(document).ready(function(){
    $("input.location_picker").each(function (i) {
        var map = document.createElement('div');
        map.className = "location_picker_map";
	$(this).parent().append($("<a href='javascript:;' onclick='loadAddress(this);' style='padding-left:5px;'>Guess</a><br/>"));
        $(this).parent().append(map);
        //$(this).css('display','none');

        var lat = 29.76019;
        var lng = -95.36933;
        if (this.value.split(',').length == 2) {
            values = this.value.split(',');
            lat = values[0];
            lng = values[1];
        }
        var center = new google.maps.LatLng(lat,lng);

	var options = {
	    zoom: 12,
	    center: center,
	    mapTypeId: google.maps.MapTypeId.ROADMAP
	};
        var map = new google.maps.Map($(".location_picker_map")[0],options);
        google.maps.event.addListener(map,'click', function(event) {
	    setLocation(event.latLng);
        });
	window.map = map;
	setLocation(center);
    });
});
