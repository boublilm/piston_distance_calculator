
# Piston Distance Calculator

Piston Assignment to calculate the distance between stickers over frames.




## Installation

Installation on Google-Colab

```bash
  !pip install -e git+https://github.com/boublilm/piston_distance_calculator.git#egg=piston_distance_calculator

  import sys
  sys.path.insert(1, '/content/src/piston-distance-calculator')

  import piston_distance_calculator    
```
    
## Usage/Examples

```python
from piston_distance_calculator import piston_difference, generate_graphs
import numpy as np

if __name__ == "__main__":
    sticker_color_dict = {
                'Yellow': (np.array([18, 93, 0]), np.array([45, 255, 255])),
                'Blue': (np.array([50, 150, 60]), np.array([100, 255, 150]))
            }

    path_list = [r"C:\Users\maorb\1.png",
                 r"C:\Users\maorb\2.png"]

    distance_list = piston_difference(path_list, sticker_color_dict['Yellow'])
    print(distance_list)
    generate_graphs(distance_list)

    path_list = [r"C:\Users\maorb\image001.jpg",
                 r"C:\Users\maorb\image002.jpg",
                 r"C:\Users\maorb\image003.jpg"]

    distance_list = piston_difference(path_list, sticker_color_dict['Blue'])
    print(distance_list)
    generate_graphs(distance_list)
```

