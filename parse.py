import json
from pathlib import Path
import random
import string

class JSMapParser(object):

    # base_dir_path: Path

    def __init__(self, base_dir_path: Path) -> None:
        self.base_dir_path = base_dir_path

    def parse(self, sourcemap_dir_path: Path):

        all_objects = sourcemap_dir_path.glob('**/*')          #all files with path
        for path in all_objects: 
                if path.is_file() and path.name[-4:] == '.map':  # parse the  .map 
                    self.sourcemap_parse(path)  
        

    def sourcemap_parse(self, file_path: Path):
        with file_path.open(mode='r', encoding='utf-8') as input_stream:
            sourcemap_data = json.loads(input_stream.read())

        if 'sources' not in sourcemap_data or 'sourcesContent' not in sourcemap_data:
            print("Sourcemap is empty or not valid")
            return
        
        for file_name, file_content in zip(sourcemap_data['sources'], sourcemap_data['sourcesContent']): # looping over and mapping sources with sourcesContent
            output_name = file_name.replace('webpack:///', '')
            output_name = output_name.replace('../', '_1')
            output_name = output_name if output_name[0] == '.' else '.' + output_name
            output_name = output_name.split('?')[0]

            full_out_name = Path(self.base_dir_path, output_name)
            try:
                full_out_name.parent.mkdir(parents=True, exist_ok=True)

                with full_out_name.open(mode='w', encoding='utf-8') as out_stream:
                    out_stream.write(file_content)
            except FileNotFoundError:
                print(f'Something wrong in sourcemap file: {file_path}, I could not save: {full_out_name}')