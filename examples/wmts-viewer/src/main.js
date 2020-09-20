import 'ol/ol.css';
import Map from 'ol/Map';
import OSM from 'ol/source/OSM';
import TileLayer from 'ol/layer/Tile';
import View from 'ol/View';
import WMTS, {optionsFromCapabilities} from 'ol/source/WMTS';
import WMTSCapabilities from 'ol/format/WMTSCapabilities';

var map;
var parser = new WMTSCapabilities();

fetch('http://brazildatacube.dpi.inpe.br/odc/ows/wmts?request=GetCapabilities&service=WMTS&version=1.0.0')
  .then(function (response) {
    return response.text();
  })
  .then(function (text) {
    var result = parser.read(text);
    var options = optionsFromCapabilities(result, {
      layer: 'CB4_64_16D_STK_1',
      matrixSet: 'WholeWorld_WebMercator',
    });

    map = new Map({
      layers: [
        new TileLayer({
          source: new OSM(),
          opacity: 0.7,
        }),
        new TileLayer({
          opacity: 1,
          source: new WMTS(options),
        }) ],
      target: 'map',
      view: new View({
        center: [-26.947547904, -61.002123],
        zoom: 5
      }),
    });
  });
