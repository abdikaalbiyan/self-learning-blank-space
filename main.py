import json
from pathlib import Path
from tqdm import tqdm
from json.decoder import JSONDecodeError


source_dir = '/Users/CTI/Documents/Academi/raw_data/movies/movies'
jsonOutputFile = 'result.json'


def main():
    jsonFiles = list(Path(source_dir).glob('*.json'))

    num_of_files = len(jsonFiles)

    loop = 1
        
    with open(jsonOutputFile, 'w') as outputFile:
        outputFile.write('[')

        with tqdm(total=num_of_files, desc="Processing Files", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
        
            for jsonFile in jsonFiles:
                try:
                    with open(jsonFile, "r") as read_file:
                        data = json.load(read_file)

                    selected_key = ['original_title', 'budget', 'genres', 'popularity', 'release_date',
                                    'revenue', 'runtime', 'vote_average', 'vote_count', 'spoken_languages']

                    output_dict = {}
                    for key, value in data.items():
                        if key in selected_key:
                            if isinstance(value, list):
                                nestedValue = []
                                for i in value:
                                    for x, y in i.items():
                                        if x == 'name':
                                            nestedValue.append(y)
                                value = ", ".join(nestedValue)
                            output_dict[key] = value
                            
                    outputFile.write(json.dumps(output_dict, ensure_ascii=False))
                    
                except JSONDecodeError as e:
                    print("Error on_data: ", jsonFile, str(e))
                    continue
                
                pbar.update(1)
                
                if loop == num_of_files:
                    break
                else:
                    outputFile.write(",")
                    loop += 1
 
        outputFile.write(']')
    print("DONE")
            

if __name__ == "__main__":
    main()