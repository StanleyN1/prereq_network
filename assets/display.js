// initialize global variables.
var edges;
var nodes;
var network;
var container;
var options, data;

// This method is responsible for drawing the graph, returns the drawn network
function drawGraph() {
    var container = document.getElementById('mynetwork');
    var data = JSON.parse(document.getElementById('graph-data').innerText);
    console.log(data)

    nodes = new vis.DataSet(data.nodes)
    edges = new vis.DataSet(data.edges)

    // adding nodes and edges to the graph
    var jdata = {nodes: nodes, edges: edges};

    var options = {
      "configure": {
          "enabled": true,
          "filter": ['physics'],
          "showButton": true
        },
      "edges": {
          "color": {
              "inherit": true
          },
          "smooth": {
              "enabled": false,
              "type": "continuous"
          }
      },
      "interaction": {
          "dragNodes": true,
          "hideEdgesOnDrag": false,
          "hideNodesOnDrag": false
      },
      "physics": {
          "enabled": true,
          "stabilization": {
              "enabled": true,
              "fit": true,
              "iterations": 1000,
              "onlyDynamicEdges": false,
              "updateInterval": 50
          },
          "barnesHut": {
            "gravitationalConstant": -4000,
            "centralGravity": 0.4,
            "springLength": 275,
            "springConstant": 0.005,
            "avoidOverlap": 0.23
          }
        },
      "width": (window.innerWidth - 50) + "px", //changes canvas size
			"height": (window.innerHeight - 55) + "px" //changes canvas size
    };




    // if this network requires displaying the configure window,
    // put it in its div
    options.configure["container"] = document.getElementById("config");


    network = new vis.Network(container, data, options);

    network.on("stabilizationProgress", function(params) {
      var widthFactor = params.iterations/params.total;
      document.getElementById('loading').innerHTML = Math.round(widthFactor*100) + '%';
  });

  network.once("stabilizationIterationsDone", function() {
      document.getElementById('loading').style.opacity = 0;
      document.getElementById('loading').style.display='none';

      // really clean the dom element
      setTimeout(function () {document.getElementById('loading').style.display = 'none';}, 500);
  });


    return network;

}
var years = ['2018S', '2018F', '2019S', '2019F', '2020S', '2020F', '2021S', '2021F',
       '2022S', '2022F', '2023S', '2023F', '2024S', '2024F', '2025S', '2025F',
       '2026S'];
function takeInput() {
  var year_chosen = document.getElementById('year-chooser').value;

  if (years.includes(year_chosen)) {
    jdata = JSON.parse(document.getElementById('graph-data').innerText);
    nodes = new vis.DataSet(jdata.nodes)
    network.setData({nodes: nodes, edges:edges});
    document.getElementById('year-chooser').value = '';
  }
}


setTimeout(drawGraph, 1000);
setInterval(takeInput, 1000);
