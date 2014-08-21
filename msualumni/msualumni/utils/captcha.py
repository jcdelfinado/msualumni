import numpy as np
from django.shortcuts import render_to_response, RequestContext


def hash(person): 
    val = 5381 
  
    user_input = person.upper() 
    for character in user_input: 
        val = (( np.left_shift(val, 5) + val) + ord(character)) 
    val = np.int32(val) 
    return val