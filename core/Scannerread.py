from pathlib import Path
class Scanner:
 @staticmethod
 def scan(path_str:str)->tuple[list[str],list[str]]:
  fpath_str = path_str.strip('"').strip("'")
  folder = Path(fpath_str)
  if not folder.is_dir():
     raise ValueError("Invalid path")
  else:
   filename = []
   foldername = []
   for file in folder.iterdir():
     if file.is_file():
        filename.append(file)
     if file.is_dir():
        foldername.append(file)
     return filename,foldername