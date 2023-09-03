from threading import Thread
from pathlib import Path, PurePath
from shutil import move, unpack_archive, ReadError
import argparse
import re

list_dir = []
file_types = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', 'svg'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', 'xls', '.ppt', '.pptx'],
        'Videos': ['.mp4', '.avi', '.mov', '.mkv'],
        'Music': ['.mp3', '.wav', '.flac', '.amr', '.ogg'],
        'Archives' : ['.zip', '.gz', '.tar']
    }



parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument('--source', '-s', required = True, help = 'Source folder')
parser.add_argument('--output', '-o', default='dist', help = 'Output folder')
args = vars(parser.parse_args())
source = Path(args.get('source'))
output = args.get('output')

output_folder = Path("/".join([str(source.parent),output])) #dist


def translate(name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    return re.sub(r'\W', '_', name.translate(TRANS))

def customize_file(file):
    return translate(PurePath(file).stem)+PurePath(file).suffix



def read_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            parse_folder = Thread(target=read_folder, args=(el,) )
            parse_folder.start()
        else :
            thread = Thread(target=sort_file, args=(el, ))
            thread.start()
              

def sort_file(file):
    try :
        sort_dir = [key for key, val in file_types.items() if file.suffix in val][0] 
    except IndexError:
        sort_dir = "Unknow_files"
    new_path = output_folder / sort_dir
    new_path.mkdir(exist_ok = True, parents=True)
    move(file, new_path / customize_file(file.name))
    
    if sort_dir == "Archives":
        th_unpack = Thread(target=archive_unpack, args=(new_path / customize_file(file.name),))
        th_unpack.start()
                   

def archive_unpack(archive):
    
    path_archive = archive.parent/archive.stem
    unpack_archive(archive, path_archive)
    try:
        unpack_archive(archive, path_archive)
        print(f"Archive: {archive.stem} successfully unpacked")
    except ReadError:
            pass


def read_folder_for_clean(path: Path) -> None:
    list_dir = []
    for el in path.iterdir():
        if el.is_dir():
            list_dir.append(el)
            list_dir += read_folder_for_clean(el)
    list_dir.append(path)
    list_dir.reverse()
    return list_dir

def delete_empty(list_dir_del):
    for dir_del in list_dir_del:
        try:
            Path(dir_del).rmdir()
            print(f"folder: {dir_del} deleted")
        except OSError:
           continue 
    
        

if  __name__ == "__main__":
    
    parse_and_move = Thread(target=read_folder, args=(source, ))
    parse_and_move.start() 
    parse_and_move.join()

    delete_empty(read_folder_for_clean(source))
    print("Finished")