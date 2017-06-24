
  var p = new google.maps.LatLng({lat: 37.805749114187385, lng: -122.4270486831665});
  //var projection = mymap.get();
  //console.log(projection); 
  var point = project(p);
  console.log("Projection:" + point.x + "," + point.y);
  var f = 1<<13;
  var bounds = [[Math.round(point.x * f/512), Math.round(point.y * f/512)]];
  console.log(bounds[0][0]/512 + "," + bounds[0][1]/512);
  var moonMapType = new google.maps.ImageMapType({
    getTileUrl: function(coord, zoom) {
        var normalizedCoord = getNormalizedCoord(coord, zoom);
        if (!normalizedCoord) {
          return null;
        }
        var bound = Math.pow(2, zoom);
        if(coord.x == bounds[0][0] && coord.y == bounds[0][1]){
            return 'file1.png';
        }
        return null;
        
    },
    tileSize: new google.maps.Size(256*2  , 256*2),
    maxZoom: 17,
    minZoom: 0,
    radius: 1738000,
    name: 'Moon'
  });

  //map.mapTypes.set('moon', moonMapType);
  //map.setMapTypeId('moon');
    mymap.overlayMapTypes.push(moonMapType);
}

// Normalizes the coords that tiles repeat across the x axis (horizontally)
// like the standard Google map tiles.
function getNormalizedCoord(coord, zoom) {
  var y = coord.y;
  var x = coord.x;
    console.log("x:" + x);
    console.log("y:" + y);

  // tile range in one direction range is dependent on zoom level
  // 0 = 1 tile, 1 = 2 tiles, 2 = 4 tiles, 3 = 8 tiles, etc
  var tileRange = 1 << zoom;

  // don't repeat across y-axis (vertically)
  if (y < 0 || y >= tileRange) {
    return null;
  }

  // repeat across x-axis
  if (x < 0 || x >= tileRange) {
    //x = (x % tileRange + tileRange) % tileRange;
      return null;
  }

  return {x: x, y: y};
}

function project(latLng) {
  TILE_SIZE = 256;
  var siny = Math.sin(latLng.lat() * Math.PI / 180);

  // Truncating to 0.9999 effectively limits latitude to 89.189. This is
  // about a third of a tile past the edge of the world tile.
  siny = Math.min(Math.max(siny, -0.9999), 0.9999);

  return new google.maps.Point(
      TILE_SIZE * (0.5 + latLng.lng() / 360),
      TILE_SIZE * (0.5 - Math.log((1 + siny) / (1 - siny)) / (4 * Math.PI)));
}