import requests
import pandas as pd

url = "https://content-us-1.content-cms.com/api/06b21b25-591a-4dd3-a189-197363ea3d1f/delivery/v1/search?q=classification:content&fl=document:%5bjson%5d&fl=type&rows=100"

response = requests.get(url)
data = response.json() 

df = pd.json_normalize(data)
df.to_json('sample.json', orient='records', lines=True, force_ascii=False, indent=4)

file_path = 'arts.json'
data = pd.read_json(file_path)


category_values = []

for doc in data['documents']:
    elements = doc.get('document', {}).get('elements', {})
    category_element = elements.get('category', {})
    categories = category_element.get('categories', [])
    
    if categories:
        category_values.extend(categories)

df_categories = pd.DataFrame(category_values, columns=['Category Name'])
category_counts = df_categories['Category Name'].value_counts().reset_index()
category_counts.columns = ['Category Name', 'frequency']

output_csv_path = 'savedCSV/results.csv'
category_counts.to_csv(output_csv_path, index=False)

