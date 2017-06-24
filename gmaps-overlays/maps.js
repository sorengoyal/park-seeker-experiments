
var overlay;
USGSOverlay.prototype = new google.maps.OverlayView();

function initMap() {
  var mymap = new google.maps.Map(document.getElementById('map'), {
    center: {lat:37.855749114187385, lng: -122.4570486831665,},
    zoom: 13,
  }); 
  // Initialize the map and the custom overlay.
  var bounds = new google.maps.LatLngBounds(
        new google.maps.LatLng(37.805749114187385, -122.497048689),
        new google.maps.LatLng(37.8957491149, -122.4270486831665));
  // The photograph is courtesy of the U.S. Geological Survey.
  var srcImage = 'file1.png';
  // The custom USGSOverlay object contains the USGS image,
  // the bounds of the image, and a reference to the map.
  overlay = new USGSOverlay(bounds, srcImage, mymap);
}

/** @constructor */
function USGSOverlay(bounds, image, mymap) {
  // Initialize all properties.
  this.bounds_ = bounds;
  this.image_ = image;
  this.map_ = mymap;
  // Define a property to hold the image's div. We'll
  // actually create this div upon receipt of the onAdd()
  // method so we'll leave it null for now.
  this.div_ = null;
  // Explicitly call setMap on this overlay.
  this.setMap(mymap);
}

/**
 * onAdd is called when the map's panes are ready and the overlay has been
 * added to the map.
 */
USGSOverlay.prototype.onAdd = function() {
  var div = document.createElement('div');
  div.style.borderStyle = 'none';
  div.style.borderWidth = '0px';
  div.style.position = 'absolute';
  // Create the img element and attach it to the div.
  var img = document.createElement('img');
  img.src = this.image_;
  img.style.width = '100%';
  img.style.height = '100%';
  img.style.position = 'absolute';
  div.appendChild(img);
  this.div_ = div;
  // Add the element to the "overlayLayer" pane.
  var panes = this.getPanes();
  panes.overlayLayer.appendChild(div);
};

USGSOverlay.prototype.draw = function() {
  // We use the south-west and north-east
  // coordinates of the overlay to peg it to the correct position and size.
  // To do this, we need to retrieve the projection from the overlay.
  var overlayProjection = this.getProjection();
  // Retrieve the south-west and north-east coordinates of this overlay
  // in LatLngs and convert them to pixel coordinates.
  // We'll use these coordinates to resize the div.
  console.log(this.bounds_);
  var sw = overlayProjection.fromLatLngToDivPixel(this.bounds_.getSouthWest());
  var ne = overlayProjection.fromLatLngToDivPixel(this.bounds_.getNorthEast());
  console.log('sw' + sw);
  console.log('ne' + ne);
  // Resize the image's div to fit the indicated dimensions.
  var div = this.div_;
  div.style.left = sw.x + 'px';
  div.style.top = ne.y + 'px';
  div.style.width = (ne.x - sw.x) + 'px';
  div.style.height = (sw.y - ne.y) + 'px';
  console.log(div);
};

// The onRemove() method will be called automatically from the API if
// we ever set the overlay's map property to 'null'.
USGSOverlay.prototype.onRemove = function() {
  this.div_.parentNode.removeChild(this.div_);
  this.div_ = null;
};

google.maps.event.addDomListener(window, 'load', initMap);