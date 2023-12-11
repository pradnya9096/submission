# Que:1
import pandas as pd

def calculate_distance_matrix(dataset_path):
    # Read the dataset into a DataFrame
    df = pd.read_csv(dataset_path)

    # Create a DataFrame with unique IDs
    unique_ids = sorted(set(df['id_start'].unique()) | set(df['id_end'].unique()))
    distance_matrix = pd.DataFrame(index=unique_ids, columns=unique_ids)

    # Initialize the matrix with 0s on the diagonal
    distance_matrix.values[[range(len(distance_matrix))]*2] = 0

    # Populate the matrix with cumulative distances
    for index, row in df.iterrows():
        distance_matrix.at[row['id_start'], row['id_end']] = row['distance']
        distance_matrix.at[row['id_end'], row['id_start']] = row['distance']

    # Calculate cumulative distances
    distance_matrix = distance_matrix.cumsum(axis=1).cumsum(axis=0)

    return distance_matrix

# Example usage
dataset_path = 'MapUp-Data-Assessment-F\datasets\dataset-3.csv'
result_matrix = calculate_distance_matrix(dataset_path)
print(result_matrix)

# Que:2
import pandas as pd

def unroll_distance_matrix(distance_matrix):
    # Reset the index to get 'id_start' as a column
    distance_matrix_reset = distance_matrix.reset_index()

    # Melt the DataFrame to convert it to the desired format
    unrolled_df = pd.melt(distance_matrix_reset, id_vars='index', var_name='id_end', value_name='distance')

    # Rename columns
    unrolled_df.columns = ['id_start', 'id_end', 'distance']

    # Filter out rows where 'id_start' is equal to 'id_end'
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]

    return unrolled_df

# Example usage
dataset_path = 'MapUp-Data-Assessment-F\datasets\dataset-3.csv'
distance_matrix = calculate_distance_matrix(dataset_path)
unrolled_result = unroll_distance_matrix(distance_matrix)
print(unrolled_result)

# Que:3
import pandas as pd

def find_ids_within_ten_percentage_threshold(distance_matrix, reference_id):
    # Calculate the average distance for the reference value
    avg_distance = distance_matrix.loc[reference_id, :].mean()

    # Calculate the lower and upper bounds within 10% of the average distance
    lower_bound = avg_distance * 0.9
    upper_bound = avg_distance * 1.1

    # Filter the 'id_start' values within the 10% threshold
    result_ids = distance_matrix.index[(distance_matrix.loc[:, reference_id] >= lower_bound) & (distance_matrix.loc[:, reference_id] <= upper_bound)].tolist()

    # Sort the result list
    result_ids.sort()

    return result_ids

# Example usage
dataset_path = 'MapUp-Data-Assessment-F\datasets\dataset-3.csv'
distance_matrix = calculate_distance_matrix(dataset_path)

# Assuming reference_id is one of the IDs in the 'id_start' column
reference_id = 1001420
result_ids = find_ids_within_ten_percentage_threshold(distance_matrix, reference_id)
print(result_ids)

# Que:4
import pandas as pd

def calculate_toll_rate(unrolled_df):
    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Calculate toll rates for each vehicle type
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        column_name = f'{vehicle_type}_toll'
        unrolled_df[column_name] = unrolled_df['distance'] * rate_coefficient

    return unrolled_df

# Example usage
dataset_path = 'MapUp-Data-Assessment-F\datasets\dataset-3.csv'
distance_matrix = calculate_distance_matrix(dataset_path)
unrolled_result = unroll_distance_matrix(distance_matrix)
result_with_toll_rates = calculate_toll_rate(unrolled_result)
print(result_with_toll_rates)

# Que:5
import pandas as pd
from datetime import datetime, timedelta, time

def calculate_time_based_toll_rates(toll_rate_df):
    # Define time ranges for weekdays and weekends
    weekday_time_ranges = [(time(0, 0, 0), time(10, 0, 0)),
                           (time(10, 0, 0), time(18, 0, 0)),
                           (time(18, 0, 0), time(23, 59, 59))]

    weekend_time_ranges = [(time(0, 0, 0), time(23, 59, 59))]

    # Function to apply discount factor based on time range
    def apply_discount(row):
        day_of_week = row['id_start']  # Replace with the actual column name
        start_time = row['id_end']  # Replace with the actual column name

        if day_of_week in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            for start_range, end_range in weekday_time_ranges:
                if start_range <= start_time <= end_range:
                    return 0.8 if start_range <= start_time <= time(10, 0, 0) else 1.2
        elif day_of_week in ['Saturday', 'Sunday']:
            return 0.7

    # Apply the discount factor for each row
    toll_rate_df['discount_factor'] = toll_rate_df.apply(apply_discount, axis=1)

    # Apply the discount factor to each vehicle type toll rate
    vehicle_columns = ['moto_toll', 'car_toll', 'rv_toll', 'bus_toll', 'truck_toll']
    for column in vehicle_columns:
        toll_rate_df[column] *= toll_rate_df['discount_factor']

    # Drop the discount_factor column
    toll_rate_df.drop('discount_factor', axis=1, inplace=True)

    return toll_rate_df

# Example usage
dataset_path = 'MapUp-Data-Assessment-F\datasets\dataset-3.csv'
distance_matrix = calculate_distance_matrix(dataset_path)
unrolled_result = unroll_distance_matrix(distance_matrix)
result_with_toll_rates = calculate_toll_rate(unrolled_result)
result_with_time_based_toll_rates = calculate_time_based_toll_rates(result_with_toll_rates)
print(result_with_time_based_toll_rates)



