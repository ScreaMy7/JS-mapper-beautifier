from pathlib import Path
from const import SOURCEMAP_SRC_DIR
from const import JS_SRC_DIR
from download import JSMapDownloader
from parse import JSMapParser
import argparse
import shutil


def arg_parser():
    parser = argparse.ArgumentParser(description="""JS Mapper & beautifier
        Usage:
        Download and beatify JS files, if its a webpack try to download and parse SourceMap files to create the folder strcture:
            python3 main.py  -i ListOfJSfiles -o DirectoryName
    """)
    parser.add_argument('-i', '--input', help='Folder with loaded sourcemap files or path to list of files that should be beautified and parsed accordinglily', required=True)
    parser.add_argument('-o', '--output', help='Where should be saved', required=True)
    
    args = parser.parse_args()

    return args


def read_file(path: Path):
    res = []
    with path.open(mode='r', encoding='utf-8') as stream:
        line = stream.readline()
        while line:
            line = line.replace('\n', '')
            res.append(line)
            line = stream.readline()

    return res

def main():
    args = arg_parser()


    input_path= Path(args.input)
    output_path = Path(args.output)

    if input_path.is_dir():
        base_path= input_path
    else:
        base_path= input_path.parent

    
    if input_path.is_file():
        base_path = input_path.parent  # where jsfile is downloaded

        sourcemap_src = Path(base_path, SOURCEMAP_SRC_DIR)
        scripts_list_path = input_path
        script_list = read_file(scripts_list_path)
        #print("js mode")
        downloads = JSMapDownloader()
        downloads.download(script_list, base_path)
    else:
        print("No js paths present")
        
        
    parser = JSMapParser(output_path) 
    parser.parse(sourcemap_src)

    # moving js_src to folder name by user
    source_js = Path(base_path, JS_SRC_DIR)
    destination_js = Path(base_path, output_path)
    shutil.move(source_js,destination_js)

    source_map = Path(base_path, SOURCEMAP_SRC_DIR)
    destination_map = Path(base_path, output_path)
    shutil.move(source_map,destination_map)

    exit(0)

        

if __name__ == '__main__':
    main()

            



























if __name__ == '__main__':
    main()