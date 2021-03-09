# Construct a Concept Graph for a Course Dataset

## Introduction

#### Cover Network
- A cover network <img src="https://render.githubusercontent.com/render/math?math=\mathcal{G}^c"> consists of concept nodes <img src="https://render.githubusercontent.com/render/math?math=\mathcal{P}"> and cover edges <img src="https://render.githubusercontent.com/render/math?math=\mathcal{L}^c \in \mathcal{P} \times \mathcal{P}">.

- A cover edge <img src="https://render.githubusercontent.com/render/math?math=p_a > p_b \in \mathcal{L}^c"> if <img src="https://render.githubusercontent.com/render/math?math=p_a \in T_i"> and <img src="https://render.githubusercontent.com/render/math?math=p_b \in s_{i,j}"> for some course <img src="https://render.githubusercontent.com/render/math?math=C_i"> and section <img src="https://render.githubusercontent.com/render/math?math=s_{i,j}">.

#### Order Network
- An order network <img src="https://render.githubusercontent.com/render/math?math=\mathcal{G}^o"> consists of concept nodes <img src="https://render.githubusercontent.com/render/math?math=\mathcal{P}"> and cover edges <img src="https://render.githubusercontent.com/render/math?math=\mathcal{L}^o \in \mathcal{P} \times \mathcal{P}">.

- An order link <img src="https://render.githubusercontent.com/render/math?math=p_a \rightarrow p_b \in \mathcal{L}^o"> if <img src="https://render.githubusercontent.com/render/math?math=p_a \in s_{i,j}"> and <img src="https://render.githubusercontent.com/render/math?math=p_b \in s_{i,j'}"> for some course <img src="https://render.githubusercontent.com/render/math?math=C_i">, section <img src="https://render.githubusercontent.com/render/math?math=s_{i,j}">, and section <img src="https://render.githubusercontent.com/render/math?math=s_{i,j'}"> such that <img src="https://render.githubusercontent.com/render/math?math=j < j'">.

Details about the order and cover network can be found [here](https://www.overleaf.com/project/5f98ffbd8a6f330001b63ac8)

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
      
- To generate the tree concept graph, please follow this command:

      $ python main_root_graph.py -concept [name of the concept] -edge [path of the edge data constructed by the main_graph.py]
      
- To apply the random walk with restart, please follow this command:

      $ python main_rwr.py -edge [path of the edge data constructed by the main_graph.py]
      
- To generate the json data for the graph visualization, please follow this command:
      
       $ python main_data.py -edge [path of the edge data constructed by the main_graph.py]

