

def flatten_array(arr):
    flat_list = []
    for sublist in arr:
        for item in sublist:
            flat_list.append(item)
            
    return flat_list

def array_to_dict(arr):

  dict = {}
  for sublist in arr:
    dict[sublist[0]] = str(sublist[1])

  return dict