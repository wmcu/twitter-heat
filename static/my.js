$(function() {
  var tweet_locations = [];
  var pointArray = new google.maps.MVCArray(tweet_locations);
  var map;
  var heatmap;
  var word = "";

  function update() {
    $.getJSON("data/" + word, function(data) {
      tweet_locations = []
      $.each(data.data, function(i, item){
        tweet_locations.push(new google.maps.LatLng(item.latitude, item.longitude));
      });
      pointArray = new google.maps.MVCArray(tweet_locations);
      heatmap.setData(pointArray);
    });
  }

  function initialize() {
    tweet_locations = [];
    pointArray = new google.maps.MVCArray(tweet_locations);

    var mapOptions = {
      center: { lat: 0, lng: 0},
      zoom: 3,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);

    heatmap = new google.maps.visualization.HeatmapLayer({
      data: pointArray
    });

    heatmap.setMap(map);
    heatmap.set('radius', 20);

    word = $("#keyword").val();
    window.setInterval(update, 1500);
  }

  $("#keyword").change(function() {
    word = $("#keyword").val();
    update();
  });

  google.maps.event.addDomListener(window, 'load', initialize);

})
