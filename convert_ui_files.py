import pyside2uic
import os


def convert_ui_files(folderpath):
    for file in os.listdir(folderpath):
        if file.endswith(".ui"):
            ui_filename = file
            file_root, file_ext = os.path.splitext(file)
            py_filename = file_root + "_ui.py"
            print("{} --> {}".format(ui_filename, py_filename))
            with open(os.path.join(folderpath, ui_filename), 'r') as ui_file:
                with open(os.path.join(folderpath, py_filename), 'w') as py_file:
                    pyside2uic.compileUi(ui_file, py_file)


if __name__ == '__main__':

    this_path = os.path.dirname(os.path.abspath(__file__))

    ui_files_path = os.path.join(this_path, 'futura_ui', 'app', 'ui', 'ui_files')

    assert os.path.isdir(ui_files_path)

    convert_ui_files(ui_files_path)
