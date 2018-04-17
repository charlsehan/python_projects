try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import os
import sys


def string_exist(str_name, reference_file):
    if not str_name:
        return False
    tree = ET.parse(reference_file)
    root = tree.getroot()
    elem = root.find("./*[@name='" + str_name + "']")
    if elem is None:
        return False
    return True


def get_reference_file(source_file):
    path_name, file_name = os.path.split(source_file)
    upper_path, language = os.path.split(path_name)
    return os.path.join(upper_path, os.path.join('values-ja', file_name))


def get_target_file(source_file):
    if source_file.endswith('.xml'):
        return source_file[:-4] + '_new' + source_file[-4:]
    else:
        return source_file + '_new'


def remove_existing_strings(source_file):
    print 'processing file: ' + source_file + ' ...'
    reference_file = get_reference_file(source_file)
    if not os.path.exists(reference_file):
        print 'not exist reference file: ' + reference_file
        return
    target_file = get_target_file(source_file)
    tree = ET.parse(source_file)
    root = tree.getroot()
    found_list = []
    for elem in root:
        if string_exist(elem.get('name', None), reference_file):
            found_list.append(elem)

    for elem in found_list:
        root.remove(elem)

    with open(target_file, 'w') as xml:
        tree.write(xml, encoding='utf-8', xml_declaration=True)


def process_one_dir(dir_path):
    print "processing " + dir_path + ' ---'
    str_files = os.listdir(dir_path)
    for f in str_files:
        if f.endswith('.xml'):
            remove_existing_strings(os.path.join(dir_path, f))


def process_all_sub_dir(dir_path):
    sub_dirs = os.listdir(dir_path)
    for sub in sub_dirs:
        if not sub.startswith('.'):
            process_one_dir(os.path.join(dir_path, os.path.join(sub, 'values')))
            process_one_dir(os.path.join(dir_path, os.path.join(sub, 'values-zh-rCN')))


def main(args):
    #process_one_dir(args[0])
    process_all_sub_dir(args[0])


if __name__ == '__main__':
    main(sys.argv[1:])
