from typing import List, Tuple, Dict
from math import floor

def downsample(texts : List[str], target : List[int], proportion_true : float) -> Tuple[List[str], List[int]]:
    
    text_per_target : Dict[int,List[str]] = {0: [], 1: []}
    
    for label, text in zip(target,texts):
        text_per_target[label].append(text)
        
    nr_true : int = len(text_per_target[1])
    nr_false : int = floor((nr_true / proportion_true) * (1-proportion_true))
    
    if nr_false > len(text_per_target[1]):
        nr_false = len(text_per_target[1])
        nr_true = floor((nr_false / (1-proportion_true)) * proportion_true)
		
    new_texts : List[str] = []
    new_target : List[int] = []
    
    for i in range(nr_false):
        new_target.append(0)
        new_texts.append(text_per_target[0][i])
	
    for i in range(nr_true):
        new_target.append(1)
        new_texts.append(text_per_target[1][i])
        
    return new_texts, new_target