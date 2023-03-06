import jsbeautifier
from pathlib import Path
import requests
from typing import List
import urllib3


from const import JS_SRC_DIR, SOURCEMAP_SRC_DIR

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # to remove unnessary exceptions

class JSMapDownloader(object):

    IS_SOURCEMAP = 1
    IS_JS = 0
    IS_UNKNOWN = -1

    def downloader(self , url: str):

        parsed_url = requests.utils.urlparse(url)

        path= parsed_url.path
        file_name = Path(path).name

        resp = requests.get(url)

        if resp.status_code == 200:
            return (file_name, resp.content.decode('utf-8'))
        else:
            return (file_name,'')



    def check(self, url):

        parsed_url = requests.utils.urlparse(url)
        path = parsed_url.path

        source_map_url = url.replace(path, f'{path}.map')
        
        #source_map_url = url+".map"
        try:
            resp = requests.head(source_map_url)
        except:
            pass

        if resp.status_code == 200:
            target_url = source_map_url
            type_of_data = self.IS_SOURCEMAP
            print("is a map->",target_url)
        else:
            target_url = url 
            type_of_data = self.IS_JS
            print("is a js file->",target_url)

        file_name, content = self.downloader(target_url)

        return (file_name, content, type_of_data)


    def download(self, urls, base_dir: Path):

        js_base_dir = Path(base_dir, JS_SRC_DIR)
        map_base_dir = Path(base_dir, SOURCEMAP_SRC_DIR)

        js_base_dir.mkdir(exist_ok=True)
        map_base_dir.mkdir(exist_ok=True)

        for url in urls:
            if url != "":  # check if nto blank new line
                file_name, content, type_of_data = self.check(url)
            
            # file_name, content, type_of_data = self.check(url)

            if type_of_data == self.IS_JS :
                if type_of_data == self.IS_JS :
                    content = jsbeautifier.beautify(content) 
                    js_open_path = Path(js_base_dir, file_name)
                    
                    with open(js_open_path, 'w' ,encoding='utf-8') as out_stream:
                        out_stream.write(content)

            if type_of_data == self.IS_SOURCEMAP:
                
                map_open_path = Path(map_base_dir, file_name)
                with open(map_open_path, 'w' ,encoding='utf-8') as out_stream:
                    out_stream.write(content)
    
        


