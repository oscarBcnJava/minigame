import os



def getResource(path_elements):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),*path_elements)