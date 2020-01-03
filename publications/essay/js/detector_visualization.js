//The main function
function initializeDetectorVisualization(element,identifier,detectors,adding_detectors_allowed)
{
    var vis_template = `<div class="interactive_panel"><h3>The detectors</h3>
    <div class="detectorArea"></div>
    <h3>The example conversations</h3>
    <div class="slider_area">
    	<div>First message</div>
	    <input class="time_slider" name="time_slider" type="range" min="0" max="199" value="0">
	    <div>Last message</div>
    </div>
    <table class="individual_player_visualizations">
        <tr><td>Game 1</td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td></tr>
        <tr><td>Game 2</td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td></tr>
        <tr><td>Game 3</td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td></tr>
        <tr><td>Game 4</td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td></tr>
        <tr><td>Game 5</td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td></tr>
        <tr><td>Game 6</td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td></tr>
        <tr><td>Game 7</td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td></tr>
        <tr><td>Game 8</td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td></tr>
        <tr><td>Game 9</td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td></tr>
        <tr><td>Game 10</td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td><td><img src="svg/tn_quiet.svg"></td></tr>
    </table>

    <h3>The evaluation</h2>
	<canvas class="true_positives" width="300" height="150" style="border:1px solid #d3d3d3;"></canvas>
    <canvas class="false_positives" width="300" height="150" style="border:1px solid #d3d3d3;"></canvas>
    </div>`

    element.innerHTML = vis_template;
    allDetectorVisualizations[identifier] = new DetectorVisualization(detectors,element);
    allDetectorVisualizations[identifier].slider.oninput = function() {allDetectorVisualizations[identifier].moveTimeSlider(allDetectorVisualizations[identifier].slider.value)};
}

//Classes to make it all clearer and better structured
class DetectorVisualization
{
	constructor(detectors,element)
	{
		this.currentTime = 0;
		this.beta = 1;
		this.currentlySelectedDetectorIndex = 0;
		this.mainElement = element;	
		this.slider = this.mainElement.getElementsByClassName('time_slider')[0];

		this.detectors = [];
		for (var detector of detectors)
		{
			var detectorType = detectorTypes[detector[0]];
			this.addDetector(detectorType,detector[1]);
		}
	}

	addDetector(detectorType,threshold)
	{
	    var detector = new Detector(detectorType,false);
	    detector.threshold = threshold;
	    detector.fscores = precalculatedResultsPerDetectorType[detectorType.identifier].fbeta;
	    this.detectors.push(detector);

	    this.updateDetectorArea();
	    this.updateGraphs();
	    this.updatePlayerVisualizations(this.currentTime,this.currentlySelectedDetectorIndex);
	}

	changeDetectorThreshold(detectorIndex,delta)
	{
	    if (delta == 1)
	    {
	        this.detectors[detectorIndex].nextThreshold();
	    }
	    else
	    {
	        this.detectors[detectorIndex].previousThreshold();
	    }

	    this.updateDetectorArea();
	    this.updateGraphs();
	    this.updatePlayerVisualizations(this.currentTime,this.currentlySelectedDetectorIndex);
	}

	moveTimeSlider(time)
	{
	    this.currentTime = time;
	    this.updatePlayerVisualizations(this.currentTime,this.currentlySelectedDetectorIndex);
	    this.updateGraphs();
	}

	moveFbetaSlider(beta_index)
	{
	    this.beta = allBetaValues[beta_index];
	    this.updateGraphs();
	}

	updateDetectorArea()
	{
		var detectorHTMLTemplate = '<div class="detector detector_{{ index }} selected" detectorIndex="{{ index }}"><div class="detectorTitle">{{ name }}</div><div class="detectorDescription">{{ description }}</div><button onClick="changeDetectorThreshold({{ index }},-1)">Lower</button><div class="detectorThreshold">{{ threshold }}</div><button onClick="changeDetectorThreshold({{ index }},1)">Higher</button></div>';

	    var detectorAreaHTML = '';

	    for (var detectorIndex in this.detectors)
	    {
	        var detector = this.detectors[detectorIndex];
	        detectorAreaHTML += detectorHTMLTemplate.replace(/{{ threshold }}/g,detector.getThreshold(this.currentTime)).replace(/{{ index }}/g,detectorIndex).replace(/{{ name }}/g,detector.detectorType.name).replace(/{{ description }}/g,detector.detectorType.description);
	    }

	    this.mainElement.getElementsByClassName('detectorArea')[0].innerHTML = detectorAreaHTML +  '<br style="clear: left;" />';

	    var allDetectorElements = this.mainElement.getElementsByClassName('detector');
	    for (var elem of allDetectorElements)
	    {
	        elem.onclick = function()
	        {
	            for (d of this.mainElement.getElementsByClassName('detector'))
	            {
	                d.classList.remove('selected');
	            }

	            this.classList.add('selected')

	            this.currentlySelectedDetectorIndex = this.getAttribute('detectorIndex');
	            this.updatePlayerVisualizations(this.currentTime,this.currentlySelectedDetectorIndex);
	        };
	    }
	}

	updatePlayerVisualizations(time,detectorIndex)
	{
	    var detector = this.detectors[detectorIndex];
	    var precalculatedResults = precalculatedResultsPerDetectorType[detector.detectorType.identifier];
	    var data_for_this_time = precalculatedResults.bool_per_player[detector.getThreshold(time)][time];
	    var player_names = Object.keys(data_for_this_time);
	    player_names.sort();

	    for (var player_index in player_names)
	    {
	        var player_name_parts = player_names[player_index].split('.');
	        var conversation_index = parseInt(player_name_parts[0][4]);
	        var player_name = parseInt(player_name_parts[1]);

	        if (player_name > 9)
	        {
	            continue;
	        }

	        var img_elem = this.mainElement.getElementsByClassName('individual_player_visualizations')[0].rows[conversation_index].cells[player_name+1].children[0];

	        if (!img_elem)
	        {
	            continue;
	        }

	        var speaking = 'quiet';

	        if (who_is_speaking[conversation_index][time] == player_name)
	        {
	        	speaking = 'speaking';
	        }

	        if (target[conversation_index] == player_name)
	        {
	            if (data_for_this_time[player_names[player_index]])
	            {
	                img_elem.src = 'svg/tp_'+speaking+'.svg';
	            }
	            else
	            {
	                img_elem.src = 'svg/fn_'+speaking+'.svg';
	            }
	        }
	        else
	        {
	            if (data_for_this_time[player_names[player_index]])
	            {
	                img_elem.src = 'svg/fp_'+speaking+'.svg';
	            }
	            else
	            {
	                img_elem.src = 'svg/tn_'+speaking+'.svg';
	            }
	        }
	    }
	}

	updateGraphs()
	{
	    var truePositiveData = [];
	    var falsePositiveData = [];
	    var fbetaData = [];

	    for (var detector_index in this.detectors)
	    {
	        var detector = this.detectors[detector_index];
	        var precalculatedResults = precalculatedResultsPerDetectorType[detector.detectorType.identifier];

	        var temp = precalculatedResults.tp;

	        truePositiveData.push(precalculatedResults.tp[detector.getThreshold(this.currentTime)]);
	        falsePositiveData.push(precalculatedResults.fp[detector.getThreshold(this.currentTime)]);
	        //fbetaData.push(precalculatedResults.fbeta[detector.getThreshold(this.currentTime)][this.beta]);
	    }

	   this.drawGraph(this.mainElement.getElementsByClassName('true_positives')[0],truePositiveData,10,this.currentTime);
	   this.drawGraph(this.mainElement.getElementsByClassName('false_positives')[0],falsePositiveData,100,this.currentTime);
	   //this.drawGraph(this.mainElement.getElementsByClassName('fbeta'),fbetaData,1,this.currentTime);
	}

	drawGraph(canvas,data,maxY,timeIndicatorPosition)
	{
	    //Preparations
	    var ctx = canvas.getContext("2d");
	    ctx.clearRect(0, 0, canvas.width, canvas.height);
	    var horizontalTickSize = canvas.width / (data[0].length-1);

	    var colors = ["31a5a5","a34734","59a334","a335a4"];

	    //The graph
	    ctx.setLineDash([5, 3]);

	    for (var series_index in data)
	    {
	       ctx.beginPath();
	        ctx.strokeStyle = "#"+colors[series_index];
	        ctx.moveTo(0, canvas.height - (data[series_index]/maxY*canvas.height));

	        for (var datapoint_index in data[series_index])
	        {
	            ctx.lineTo(datapoint_index*horizontalTickSize, canvas.height-(data[series_index][datapoint_index]/maxY*canvas.height));
	            ctx.stroke();
	        }
	    }

	    //The time indicator
	    ctx.beginPath();
	    ctx.setLineDash([1,0]);
	    ctx.strokeStyle = "#000000";
	    ctx.moveTo(timeIndicatorPosition*horizontalTickSize, 0);
	    ctx.lineTo(timeIndicatorPosition*horizontalTickSize, canvas.height);
	    ctx.stroke();

	}	
}

class DetectorType
{
	constructor(identifier,name,description,modelIdentifier,possibleThresholds)
	{
		this.identifier = identifier;
		this.name = name;
		this.description = description;
		this.modelIdentifier = modelIdentifier;
		this.possibleThresholds = possibleThresholds;
	}	
}

class PrecalculatedResults
{
	constructor(tp,fp,fbeta,bool_per_player)
	{
		this.tp = tp;
		this.fp = fp;
		this.fbeta = fbeta;
		this.bool_per_player = bool_per_player;
	}	
}

class Detector
{
    constructor(detectorType,useSlidingThreshold)
    {
        this.detectorType = detectorType;
        this.useSlidingThreshold = useSlidingThreshold;

        this.staticThresholds = detectorType.possibleThresholds;

        //If using the sliding threshold
        this.fscores = [];

        //If not using the sliding threshold
        this.staticThresholdIndex = 0;
    };

    previousThreshold()
    {
        this.staticThresholdIndex--;

        if (this.staticThresholdIndex < 0)
        {
            this.staticThresholdIndex = 0;
        }
    }

    nextThreshold()
    {
        this.staticThresholdIndex++;

        if (this.staticThresholdIndex == this.staticThresholds.length)
        {
            this.staticThresholdIndex--;
        }
    }

    getThreshold(time)
    {
        if (!this.useSlidingThreshold)
        {
            return this.staticThresholds[this.staticThresholdIndex];
        }

        var best_threshold = this.staticThresholds[0];
        var highest_fscore = 0;

        for (var threshold of this.staticThresholds)
        {
            var fscore = this.fscores[threshold][1][time];

            if (fscore > highest_fscore)
            {
                highest_fscore = fscore;
                best_threshold = threshold;
            }
        }

        return best_threshold;
    }

}

var loadJS = function(url, location, successFunction)
{
    var scriptTag = document.createElement('script');
    scriptTag.src = url;
    location.appendChild(scriptTag);
    scriptTag.onload = function()
    {
    	successFunction();
    };
};

function loadPrecalculatedData(successFunction)
{
	var nrOfExternalDataScriptsLoaded = 0;

	loadJS('precalculated_data/target.js', document.body, function()
	            	{
	            		nrOfExternalDataScriptsLoaded++;
	            	});

	loadJS('precalculated_data/who_is_speaking.js', document.body, function()
	            	{
	            		nrOfExternalDataScriptsLoaded++;
	            	});

	for (var detectorTypeName in detectorTypes)
	{
		var detectorType = detectorTypes[detectorTypeName];

	    tp[detectorType.modelIdentifier] = {};
	    fp[detectorType.modelIdentifier] = {};
	    fbeta[detectorType.modelIdentifier] = {};
	    bool_per_player[detectorType.modelIdentifier] = {};

	    for (var threshold of detectorType.possibleThresholds)
	    {
	        for (var metric of ['tp','fp','fbeta','per_player'])
	        {
	            loadJS('precalculated_data/'+detectorType.modelIdentifier+'@'+threshold+'/'+metric+'.js',document.body, function()
            	{
            		nrOfExternalDataScriptsLoaded++;

            		if (nrOfExternalDataScriptsLoaded == 94)
            		{
            			successFunction();
            		}
            	});
	        }
	    }

	    precalculatedResultsPerDetectorType[detectorType.identifier] = new PrecalculatedResults(tp[detectorType.modelIdentifier],fp[detectorType.modelIdentifier],fbeta[detectorType.modelIdentifier],bool_per_player[detectorType.modelIdentifier]);
	}
}


//Define some general stuff
var allBetaValues = [0.001,0.01,0.1,1,10,100,1000];
var detectorTypes = {'dic':new DetectorType('dic','Word list detector','This is a description','m04',[1,2,3,4,5,6,7,8,9,10]),
					 'bigru_embeddings':new DetectorType('bigru_embeddings','Embeddings detector','This is a description','m02',[0.001,0.0025,0.005,0.0075,0.01,0.025,0.05,0.075,0.1,0.25,0.5,0.75,1])}

var precalculatedResultsPerDetectorType = {};
var allDetectorVisualizations = {};

var tp = {};
var fp = {};
var fbeta = {};
var bool_per_player = {};