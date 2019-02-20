from typing import List, Tuple
from numpy import array, arange, cumsum #type: ignore

import matplotlib #type: ignore
matplotlib.use('agg') #prevents a tKinter error

from matplotlib import pyplot #type: ignore
from matplotlib.legend import Legend, Rectangle #type: ignore
from matplotlib.figure import Figure #type: ignore
from matplotlib.axes._subplots import Axes #type: ignore

from hare.main import Hare

def visualize_toxicity_for_one_conversation(hare_obj : Hare, conversation_index : int =0) -> None:

    # Make sure the hare obj is up-to-date
    hare_obj.update_status_history_for_conversation(conversation_index)

    # Create the x and y data
    speakers : List[str] = list(hare_obj.conversations[conversation_index].all_speakers)
    y : List[List[float]] = [[] for speaker in speakers]

    for status in hare_obj.status_per_conversation[conversation_index]:
        for series, speaker in zip(y, speakers):

            try:
                series.append(status[speaker])
            except KeyError:
                series.append(0)

    try:
        x : array = arange(len(y[0]))
    except IndexError:
        return

    y_stack : array = cumsum(y, axis=0)

    # Create the figure, basic settings
    fig : Figure = pyplot.figure()
    ax1 : Axes = fig.add_subplot(111)
    ax1.set_xlim([0, len(x) - 1])
    ax1.set_title('Toxicity per player')
    ax1.set_xlabel('# of turns')
    ax1.set_ylabel('Toxicity')

    # Figure out the horizontal ticks (and font for vertical)
    TICK_FREQUENCY : int = 1
    x_ticks : List[int] = []
    x_tick_labels : List[int] = []

    for i in x:
        x_ticks.append(int(i))
        x_tick_labels.append(int(i + 1))

    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(x_tick_labels)

    # Draw the figure
    colors : List[Tuple[float, float, float]] = [(248 / 255, 118 / 255, 109 / 255), (205 / 255, 150 / 255, 0 / 255), (124 / 255, 174 / 255, 1 / 255),
              (0 / 255, 190 / 255, 103 / 255), (0 / 255, 191 / 255, 196 / 255), (0 / 255, 169 / 255, 1.0)]

    for i in range(len(y)):

        if i == 0:
            starting_point = 0
        else:
            starting_point = y_stack[i - 1, :]

        ax1.fill_between(x, starting_point, y_stack[i, :], color=colors[i], facecolor=colors[i])

    # Legend
    legend_color_items : List[Rectangle] = [Rectangle((0, 0), 1, 1, fc=color, edgecolor="white") for color in colors]
    legend : Legend = ax1.legend(legend_color_items, speakers, loc='upper left', prop={'size': 10})
    legend.get_frame().set_linewidth(0.5)

    pyplot.margins(y=0)
    pyplot.show(y)

def get_metric_during_conversations(hare_obj : Hare,metric_name : str) -> List[float]:

    hare_obj.update_all_status_histories()
    length_of_longest_conversation : int = max(len(conversation) for conversation in hare_obj.conversations)
    scores : List[float] = []

    for utterance_index in range(length_of_longest_conversation):
        method = getattr(hare_obj,'calculate_'+metric_name+'_at_utterance')
        scores.append(method(utterance_index))

    return scores

def visualize_accuracy_during_conversations(hare_obj : Hare):

    accuracies : List[float] = get_metric_during_conversations(hare_obj,'accuracy')
    print(accuracies)
    return

def visualize_auc_during_conversations(hare_obj : Hare):

    accuracies : List[float] = get_metric_during_conversations(hare_obj,'auc')
    print(accuracies)
    return

def visualize_fscore_during_conversations(hare_obj : Hare):

    accuracies : List[float] = get_metric_during_conversations(hare_obj,'fscore')
    print(accuracies)
    return
