# Que-1
import pandas as pd

def generate_car_matrix(dataset1):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(r"MapUp-Data-Assessment-F\datasets\dataset-1.csv")

    # Pivot the DataFrame to create the desired matrix
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)

    # Set the diagonal values to 0
    car_matrix.values[[range(len(car_matrix))]*2] = 0

    # Create a style object to highlight values
    styles = car_matrix.style.applymap(lambda x: 'color: red' if x == -1 else ('color: green' if x == 0 else ''))

    return styles
# Example usage
dataset_path = r"MapUp-Data-Assessment-F\datasets\dataset-1.csv"
result_matrix = generate_car_matrix(dataset_path)
print(result_matrix)

# Que-2
import pandas as pd

def get_type_count(df):
    # Add a new column 'car_type' based on the conditions
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    # Calculate the count of occurrences for each car_type category
    type_count = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    sorted_type_count = dict(sorted(type_count.items()))

    return sorted_type_count
# Example usage
# dataset_path = 'MapUp-Data-Assessment-F\datasets\dataset-1.csv'
df = pd.read_csv(r"MapUp-Data-Assessment-F\datasets\dataset-1.csv")
result = get_type_count(df)
print(result)

Que:3
import pandas as pd

def get_bus_indexes(df):
    # Calculate the mean value of the 'bus' column
    mean_bus = df['bus'].mean()

    # Identify indices where the 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * mean_bus].index.tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes

# Example usage
# dataset_path = r"C:\Users\LENOVO\Downloads\dataset-1.csv"
df = pd.read_csv("MapUp-Data-Assessment-F\datasets\dataset-1.csv")
result = get_bus_indexes(df)
print(result)

Que:4
import pandas as pd

def filter_routes(df):
    # Filter routes based on the condition: average truck value > 7
    selected_routes = df.groupby('route')['truck'].mean().loc[lambda x: x > 7].index.tolist()

    # Sort the list of selected routes
    selected_routes.sort()

    return selected_routes

# Example usage
# dataset_path = r"C:\Users\LENOVO\Downloads\dataset-1.csv"
df = pd.read_csv("MapUp-Data-Assessment-F\datasets\dataset-1.csv")
result = filter_routes(df)
print(result)

# Que:5
import pandas as pd

def generate_car_matrix(dataset_path):
    df = pd.read_csv(dataset_path)
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    car_matrix.values[[range(len(car_matrix))]*2] = 0
    return car_matrix

def multiply_matrix(car_matrix):
    modified_matrix = car_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    modified_matrix = modified_matrix.round(1)
    return modified_matrix

# Example usage
dataset_path = 'MapUp-Data-Assessment-F\datasets\dataset-1.csv'
result_matrix = generate_car_matrix(dataset_path)
modified_result = multiply_matrix(result_matrix)
print(modified_result)

# Que:6

import pandas as pd

def check_time_completeness(df):
    # Combine 'startDay' and 'startTime' to create a 'start_timestamp' column
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format='%A %H:%M:%S')

    # Combine 'endDay' and 'endTime' to create an 'end_timestamp' column
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format='%A %H:%M:%S')

    # Check if each (id, id_2) pair has incorrect timestamps
    completeness_check = (
        df.groupby(['id', 'id_2'])
        .apply(lambda group: (
            group['start_timestamp'].min() != pd.to_datetime(group['startDay'].min() + ' 00:00:00', format='%A %H:%M:%S') or
            group['end_timestamp'].max() != pd.to_datetime(group['endDay'].max() + ' 23:59:59', format='%A %H:%M:%S') or
            set(group['start_timestamp'].dt.weekday) != set(range(7))
        ))
    )

    return completeness_check

# Example usage
dataset_path = 'MapUp-Data-Assessment-F\datasets\dataset-2.csv'
df = pd.read_csv(dataset_path)
result = check_time_completeness(df)
print(result)



