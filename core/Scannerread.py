from pathlib import Path
class Scanner:
 @staticmethod
 def scan(path_str:str)->tuple[list[Path],list[Path]]:
  fpath_str = path_str.strip('"').strip("'")
  folder = Path(fpath_str)
  if not folder.is_dir():
    raise ValueError("Invalid path")
  filenames = []
  foldernames = []
  for item in folder.iterdir():
    if item.is_file():
      filenames.append(item)
    elif item.is_dir():
        foldernames.append(item)
  return filenames,foldernames