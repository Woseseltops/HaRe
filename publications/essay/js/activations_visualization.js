class NeuronActivationsVisualization
{
	constructor(element,activations,interesting_neurons_layer_1,interesting_neurons_layer_2)
	{
		this.activations = activations;
		this.lastHoveredWordIndex = 0;
		this.showLinebreaks = true;

		//Create the static button area
		var innerHTML = '<div id="button_area"><table><tr><td>Layer 1</td>';
		var buttonIndex = 0;

		for (var neuron_index of interesting_neurons_layer_1)
		{
			innerHTML += '<td><div class="neuron_button" button_index='+buttonIndex+' layer_index=1 neuron_index='+neuron_index+'>Example neuron '+neuron_index+'</div></td>';
			buttonIndex++;
		}

		innerHTML += '</tr><tr><td>Layer 2</td>'

		for (var neuron_index of interesting_neurons_layer_2)
		{
			innerHTML += '<td><div class="neuron_button" button_index='+buttonIndex+' layer_index=2 neuron_index='+neuron_index+'>Example neuron '+neuron_index+'</div></td>';
			buttonIndex++;
		}

		innerHTML += '</tr></table></div><div id="activation_area"></div>';
		element.innerHTML = innerHTML;

		var baseObject = this; //Saving outside of the 'this' namespace
		for (var button of document.getElementsByClassName('neuron_button'))
		{			
			button.addEventListener("click",function()
			{
				baseObject.clickButton(this.getAttribute('button_index'));
				baseObject.updateActivations(this.getAttribute('layer_index'),this.getAttribute('neuron_index'));
			});
		}

		//Create the activation area
		this.activationArea = document.getElementById('activation_area');;

		this.clickButton(0);
		this.updateButtonColors(0);
		this.updateActivations(1,interesting_neurons_layer_1[0]);
	}

	updateActivations(layer,neuron)
	{
		var layer = parseInt(layer);
		var neuron = parseInt(neuron);

		var innerHTML = '<div class="sentence">';
		var word;
		var hue;

		var wordIndex = 0;

		for (var activation of this.activations[layer])
		{
			word = activation[0];
			hue = this.activationToHue(activation[neuron+1]);

			if (word == 'linebreak' && this.showLinebreaks)
			{
				innerHTML += '</div><div class="sentence">';
			}
			else
			{
				innerHTML += '<div class="word" style="background-color: hsl('+hue+', 72%, 49%, 0.8)" word_index='+wordIndex+'>' + word + '</div>';
			}

			wordIndex++;
		}

		this.activationArea.innerHTML = innerHTML+'</div>';

		var baseObject = this; //Saving outside of the 'this' namespace
		for (var word of document.getElementsByClassName('word'))
		{
			word.addEventListener("mouseover",function()
			{
				var indexOfHoveredWord = this.getAttribute('word_index');
				baseObject.updateButtonColors(indexOfHoveredWord);
			});
		}
	}

	clickButton(clickButtonIndex)
	{
		console.log(clickButtonIndex);
		var clickButtonIndex = parseInt(clickButtonIndex);
		var buttonIndex = 0;

		for (var button of document.getElementsByClassName('neuron_button'))
		{
			if (buttonIndex == clickButtonIndex)
			{
				button.classList.add('selected');
			}
			else
			{
				button.classList.remove('selected');
			}

			buttonIndex++;
		}

		this.updateButtonColors(this.lastHoveredWordIndex);
	}

	updateButtonColors(wordIndex)
	{
		for (var button of document.getElementsByClassName('neuron_button'))
		{			
			var layerIndex = parseInt(button.getAttribute('layer_index'));
			var neuronIndex = parseInt(button.getAttribute('neuron_index'));
			var hue = this.activationToHue(this.activations[layerIndex][wordIndex][neuronIndex+1]);
			
			if (button.classList.contains('selected'))
			{
				button.style.color = 'white';
				button.style.backgroundColor = 'hsl('+hue+', 72%, 49%, 0.8)';				
			}
			else
			{
				button.style.color = 'hsl('+hue+', 72%, 49%, 0.8)';		
				button.style.backgroundColor = null;						
			}
		}

		this.lastHoveredWordIndex = wordIndex;
	}

	activationToHue(activation)
	{
		var hueRange = 125;
		var normalized_activation = (activation*0.5)+0.5;
		return normalized_activation*hueRange;
	}
}