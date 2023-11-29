import pandas as pd
from random import random
import numpy as np
from math import floor
class K_Means:
    def __init__(self, 
                 data: pd.DataFrame,
                 k: int):
        self.data = data[sorted(data.columns)]
        self.data['centroid_number'] = None
        self.k = k
        self.data_columns = data.columns

        # create the initials centroids
        self.centroids = [np.array([random() for j in range(len(data.columns))]) for i in range(k)]
    """Implementation of the K-means algorithm"""
    def train(self, max_iter: int) -> [float]:
        i = 1
        while True:
            current_centroids = self.data['centroid_number']
            new_centroids = []
            for (index, row) in self.data.iterrows():
                current_vector = np.array(row[self.data_columns])

                # find the closest centroid
                min_distances_to_centroid = [np.linalg.norm(self.centroids[i]-current_vector) for i in range(self.k)]
                min_centroid = np.argmin(min_distances_to_centroid)

                new_centroids.append(min_centroid)
        
            # check if there was a change in the centroids
            if (new_centroids==current_centroids).sum() == len(new_centroids) or i == max_iter:
                print(f'Convergence reached in {i} iterations')
                break
            
            self.data['centroid_number'] = pd.Series(new_centroids)
            
            # update the centroids values
            num_examples_per_centroid = self.data['centroid_number'].value_counts()
            new_centroids_values = self.data.groupby(by=['centroid_number'], as_index=False).sum()
            new_centroids_values = pd.pivot_table(new_centroids_values, columns=['centroid_number'])
            
            for c in new_centroids_values.columns:
                new_centroids_values[c] = new_centroids_values[c]/num_examples_per_centroid[c]
            
            for c in new_centroids_values.columns:
                self.centroids[c] = np.array(new_centroids_values[c])
            
            i += 1

        self.centroids = [[floor(val) for val in c] for c in self.centroids]

    def get_data(self) -> pd.DataFrame:
        return self.data
    
    def get_data_with_new_category(self) -> pd.DataFrame:
        df_copy = self.data.copy()

        df_copy['centroid_value'] = df_copy['centroid_number'].apply(lambda c: self.centroids[c])
        return df_copy