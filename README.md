# Construct a Concept Graph for a Course Dataset

## Implementation Environment

Please install the neccessary libraries before running our tool:

- python
- tqdm

## Hyperparameters (main.graph):

* -threshold: Threshold to construct the net graph for the cover and order graph (default: 0.1). 

## Running
      
- To generate the cover graph, please follow this command: 

      $ python main_graph.py -concept [path of the concept dictionary] -course [path of the course data] -option cover

- To generate the order graph, please follow this command: 

      $ python main_graph.py -concept [path of the concept dictionary] -course [path of the course data] -option order
      
- To generate the json data for the graph website, please follow this command:
      
       $ python main_data.py -edge [path of the edge data constructed by the main_graph.py]

