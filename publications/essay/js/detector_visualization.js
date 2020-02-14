//The main function
function initializeDetectorVisualization(element,identifier,detectors,staticDetectors)
{
	var addDetectorButtons = '';

	if (!staticDetectors)
	{
		addDetectorButtons = '<button onclick="addDetectorToPlayground(\'dic\')"></button><button onclick="addDetectorToPlayground(\'bigru_embeddings\')"></button>'
	}

    var vis_template = `<div class="interactive_panel detector_panel"><h3>The detectors</h3>
    `+addDetectorButtons+`
    <div class="detectorArea"></div>
    <h3>The example conversations</h3>
    <div class="slider_area">
    	<div class="slider_explanation">First message</div>
	    <input class="time_slider" name="time_slider" type="range" min="0" max="199" value="0">
	    <div class="slider_explanation">Last message</div>
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
    <table>
    <tr><td><img class="label_illustration" src="svg/tp_quiet.svg">Toxic players correctly detected</td><td><img class="label_illustration" src="svg/fp_quiet.svg">False alarms</td></tr>
	<tr><td><div class="axisArea"><div>10</div><div class="bottom_tick">0</div></div><canvas class="true_positives" width="300" height="150"></canvas></td>
    <td><div class="axisArea"><div>30</div><div class="bottom_tick">0</div></div><canvas class="false_positives" width="300" height="150"></canvas></td>
    </tr></table>
    </div>`

    element.innerHTML = vis_template;
    allDetectorVisualizations[identifier] = new DetectorVisualization(detectors,element,staticDetectors);
    allDetectorVisualizations[identifier].slider.oninput = function() {allDetectorVisualizations[identifier].moveTimeSlider(allDetectorVisualizations[identifier].slider.value)};
}

//Classes to make it all clearer and better structured
class DetectorVisualization
{
	constructor(detectors,element,staticDetectors)
	{
		this.currentTime = 0;
		this.beta = 1;
		this.currentlySelectedDetectorIndex = 0;
		this.mainElement = element;	
		this.slider = this.mainElement.getElementsByClassName('time_slider')[0];
		this.staticDetectors = staticDetectors;

		this.detectors = [];
		for (var detector of detectors)
		{
			var detectorType = detectorTypes[detector[0]];
			this.addDetector(detectorType,detector[1]);
		}
	}

	addDetector(detectorType,thresholdIndex)
	{
	    var detector = new Detector(detectorType,false);
	    detector.staticThresholdIndex = thresholdIndex;
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
		var upArrow = '';
		var downArrow = '';

		if (!this.staticDetectors)
		{
			upArrow = '<button class="arrowButton upArrow" onclick="changePlaygroundDetectorThreshold({{ index }},1)"></button>';
			downArrow = '<button class="arrowButton downArrow" onclick="changePlaygroundDetectorThreshold({{ index }},-1)"></button>';
		}

		var detectorHTMLTemplate = '<div class="detector detector_{{ index }} {{ selected }} " detectorIndex="{{ index }}"><div class="descriptionArea"><div class="detectorTitle">{{ name }}</div><div class="detectorDescription">{{ description }}</div></div><div class="thresholdArea">'+upArrow+'{{ threshold }}'+downArrow+'</div></div>';

		//Save button code for later
		//<button onClick="changeDetectorThreshold({{ index }},-1)">Lower</button><div class="detectorThreshold">{{ threshold }}</div><button onClick="changeDetectorThreshold({{ index }},1)">Higher</button>

	    var detectorAreaHTML = '';

	    for (var detectorIndex in this.detectors)
	    {
	        var detector = this.detectors[detectorIndex];
	        var selected = '';

	        if (detectorIndex == 0)
	        {
	        	selected = 'selected'
	        }

	        var thresholdString = detector.getThreshold(this.currentTime) + '';
	        thresholdString = thresholdString.replace('0.','.');

	        detectorAreaHTML += detectorHTMLTemplate.replace(/{{ threshold }}/g,thresholdString).replace(/{{ index }}/g,detectorIndex%4).replace(/{{ name }}/g,detector.detectorType.name).replace(/{{ description }}/g,detector.detectorType.description).replace(/{{ selected }}/g,selected);
	    }

	    this.mainElement.getElementsByClassName('detectorArea')[0].innerHTML = detectorAreaHTML +  '<br style="clear: left;" />';

	    var allDetectorElements = this.mainElement.getElementsByClassName('detector');
	    var parent = this;

	    for (var elem of allDetectorElements)
	    {
	        elem.onclick = function()
	        {
	            for (var d of allDetectorElements)
	            {
	                d.classList.remove('selected');
	            }

	            parent.currentlySelectedDetectorIndex = this.getAttribute('detectorIndex');
	            allDetectorElements[parent.currentlySelectedDetectorIndex].classList.add('selected')

	            parent.updatePlayerVisualizations(parent.currentTime,parent.currentlySelectedDetectorIndex);
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
	   this.drawGraph(this.mainElement.getElementsByClassName('false_positives')[0],falsePositiveData,40,this.currentTime);
	   //this.drawGraph(this.mainElement.getElementsByClassName('fbeta')[0],fbetaData,1,this.currentTime);
	}

	drawGraph(canvas,data,maxY,timeIndicatorPosition)
	{
	    //Preparations
	    var ctx = canvas.getContext("2d");
	    ctx.clearRect(0, 0, canvas.width, canvas.height);
	    var horizontalTickSize = canvas.width / (data[0].length-1);

	    var colors = ["c59781","91c581","8981c5","c58182"];

	    //The graph
	    ctx.setLineDash([5, 3]);

	    for (var series_index in data)
	    {
	       ctx.beginPath();
	        ctx.strokeStyle = "#"+colors[series_index%4];
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

function addDetectorToPlayground(detectorType)
{
	allDetectorVisualizations['playground'].addDetector(detectorTypes[detectorType],0);	
}

function changePlaygroundDetectorThreshold(detectorIndex,thresholdIndexDelta)
{
	var playground = allDetectorVisualizations['playground'];
	var detector = playground.detectors[detectorIndex];

	if (thresholdIndexDelta == -1)
	{
		detector.previousThreshold();
	}
	else if (thresholdIndexDelta == 1)
	{
		detector.nextThreshold();
	}

	playground.updateDetectorArea();
	playground.updateGraphs();
	playground.updatePlayerVisualizations(playground.currentTime,playground.currentlySelectedDetectorIndex);
}

//Define some general stuff
var allBetaValues = [0.001,0.01,0.1,1,10,100,1000];
var detectorTypes = {'dic':new DetectorType('dic','Word list detector','A player is toxic above this number of bad words','m04',[1,2,3,4,5,6,7,8,9,10]),
					 'bigru_embeddings':new DetectorType('bigru_embeddings','Neural net detector','A player is toxic above this confidence','m02',[0.001,0.0025,0.005,0.0075,0.01,0.025,0.05,0.075,0.1,0.25,0.5,0.75,1])}

var precalculatedResultsPerDetectorType = {};
var allDetectorVisualizations = {};

var tp = {};
var fp = {};
var fbeta = {};
var bool_per_player = {};