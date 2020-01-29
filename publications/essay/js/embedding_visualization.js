function initializeEmbeddingVisualization(x,y,z,labels)
{
	for (var label in labels)
	{
		labels[label] += label;
	}

	var data = [{
		x:x, y:y, z:z,
	  hoverinfo: 'text',
		mode: 'markers',
		marker:{color: 'hsl(198, 37%, 53%)', size: 4},
		type: 'scatter3d',
	  text: labels
	}];

	var layout = {margin: {
		l: 0,
		r: 0,
		b: 0,
		t: 0
	  },
		scene: {camera: {up:{x: 0, y: 0, z: 1},center:{x: 0, y: 0, z: 0},eye:{x: 0.8, y: 0.8, z:0.9}}}};
	Plotly.newPlot('embedding_visualization', data, layout, {displaylogo: false});	
}

function highlightScatterPointsWithIndices(indices,total_nr_of_points)
{
	var colors = []

	for (var index = 0; index < total_nr_of_points; index++)
	{
		if (indices.includes(index))
		{
			colors.push('hsl(29, 98%, 57%)')			
		}
		else
		{
			colors.push('hsl(198, 37%, 53%)')
		}
	}

	var recolor = {marker:{color: colors, size: 4}};
	Plotly.restyle('embedding_visualization', recolor,[0]);	
}