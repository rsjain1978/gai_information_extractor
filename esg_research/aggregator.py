import pandas as pd
import numpy as np

def aggregate_rows_by_name(df, name):
    filtered_df = df[df['name'] == name]
    
    aggregated_data = {
        'name': name,
        'carbon_emission_target_year': '\n'.join(filtered_df['carbon_emission_target_year'].drop_duplicates().dropna()),
        'carbon_emission_target': '\n'.join(filtered_df['carbon_emission_target'].drop_duplicates().dropna()),
        'key_committements': '\n'.join(filtered_df['key_committements'].drop_duplicates().dropna()),
        'policies': '\n'.join(filtered_df['policies'].drop_duplicates().dropna()),
        'environment': '\n'.join(filtered_df['environment'].drop_duplicates().dropna()),
        'employees': '\n'.join(filtered_df['employees'].drop_duplicates().dropna()),
        'fund': '\n'.join(filtered_df['fund'].drop_duplicates().dropna()),
        'aum': '\n'.join(filtered_df['aum'].drop_duplicates().dropna()),
        'oversight': '\n'.join(filtered_df['oversight'].drop_duplicates().dropna()),
        'incentives': '\n'.join(filtered_df['incentives'].drop_duplicates().dropna()),
        'key_speakers': '\n'.join(filtered_df['key_speakers'].drop_duplicates().dropna())
    }

    return pd.DataFrame([aggregated_data])

def aggregate_all_names(df):
    unique_names = df['name'].unique()
    aggregated_dfs = [aggregate_rows_by_name(df, name) for name in unique_names]
    return pd.concat(aggregated_dfs).reset_index(drop=True)

# Example usage:
df = pd.read_csv('esg_information.csv')

aggregated_df = aggregate_all_names(df)
aggregated_df.to_csv('company_wise_esg_info.csv',index=False)
print(aggregated_df)