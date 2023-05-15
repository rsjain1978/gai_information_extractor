import pandas as pd
import numpy as np

def aggregate_rows_by_name(df, name):
    filtered_df = df[df['name'] == name]
    
    aggregated_data = {
        'name': name,
        'fair_value': '\n'.join(filtered_df['fair_value'].drop_duplicates().dropna()),
        'uncertainity': '\n'.join(filtered_df['uncertainity'].drop_duplicates().dropna()),
        'consider_buy': '\n'.join(filtered_df['consider_buy'].drop_duplicates().dropna()),
        'consider_sell': '\n'.join(filtered_df['consider_sell'].drop_duplicates().dropna()),
        'bullish_views': '\n'.join(filtered_df['bullish_views'].drop_duplicates().dropna()),
        'bearish_views': '\n'.join(filtered_df['bearish_views'].drop_duplicates().dropna()),
        'macro_views': '\n'.join(filtered_df['macro_views'].drop_duplicates().dropna()),
        'interesting_numbers': '\n'.join(filtered_df['interesting_numbers'].drop_duplicates().dropna()),
    }

    return pd.DataFrame([aggregated_data])

def aggregate_all_names(df):
    unique_names = df['name'].unique()
    aggregated_dfs = [aggregate_rows_by_name(df, name) for name in unique_names]
    return pd.concat(aggregated_dfs).reset_index(drop=True)

# Example usage:
df = pd.read_csv('./data/output/raw/eq_research_information-tmp.csv')

aggregated_df = aggregate_all_names(df)
aggregated_df.to_csv('./data/output/final/aggregated-tmp.csv',index=False)
print(aggregated_df)