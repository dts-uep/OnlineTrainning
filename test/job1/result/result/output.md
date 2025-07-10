## *This is a Markdown cell*


```python
# Code cell python
import numpy as np
import pandas as pd
import os
```


```python
print("Hello World")
```

    Hello World



```python
array = np.asarray([1,2,3])
array
```




    array([1, 2, 3])




```python
data = {
    "ID": [1, 2, 3, 4, 5],
    "Name": ['A', 'B', 'C', 'D', 'E'],
    "Job": ['BA', 'DA', 'DE', 'MN', 'DC']
}
df = pd.DataFrame(data)
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ID</th>
      <th>Name</th>
      <th>Job</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>A</td>
      <td>BA</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>B</td>
      <td>DA</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>C</td>
      <td>DE</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>D</td>
      <td>MN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>E</td>
      <td>DC</td>
    </tr>
  </tbody>
</table>
</div>




```python
save_dir = os.getenv("OUTPUT_DIR")
save_path = os.path.join(save_dir, "test_data.csv")
```


```python
df.to_csv(save_path, index=False)
```
