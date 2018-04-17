try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import zipfile
import os
import subprocess


NAME_SECURE = 'secure'
NAME_RELEASE_NOTE = 'release_note'

PROP_NAME_DICT = {
    'ro.product.name':              'product',
    'ro.product.variant':           'variant',
    'ro.build.formal':              'formal',
    'ro.build.type':                'build_type',
    'ro.build.datetime':            'build_time',
    'ro.build.version.incremental': 'incremental',
    'ro.build.display.id':          'display_version',
}

try:
    PRODUCT_NAME = os.environ['TARGET_PRODUCT']
except KeyError as e:
    PRODUCT_NAME = 'E601'
    print 'KeyError: ' + str(e)

PRODUCT_OUT_DIR = 'out/target/product/{0}'.format(PRODUCT_NAME)

BUILD_PROP = os.path.join(PRODUCT_OUT_DIR, 'system/build.prop')
RELEASE_NOTE = os.path.join(PRODUCT_OUT_DIR, 'release_note.txt')
OTA_PACKAGE_BACKUP = os.path.join(PRODUCT_OUT_DIR, 'ota_package_backup.zip')
INFO_XML = os.path.join(PRODUCT_OUT_DIR, 'info.xml')
INFO_FILE_VERSION = '1'
MBN_FILE1 = os.path.join(PRODUCT_OUT_DIR, 'sbl1.mbn')
MBN_FILE2 = os.path.join(PRODUCT_OUT_DIR, 'hyp.mbn')


def read_properties(file_prop):
    info_dict = {}
    with open(file_prop) as f:
        for line in f:
            pos = line.find('#')
            if pos > -1:
                line = line[:pos]
            ar = line.split('=')
            if len(ar) < 2:
                continue
            prop, value = ar[0].strip(), ar[1].strip()
            if prop in PROP_NAME_DICT.keys():
                info_dict[PROP_NAME_DICT[prop]] = value
    return info_dict


def is_secure():
    out1 = subprocess.call(['grep', '-i', 'cloudminds', MBN_FILE1])
    out2 = subprocess.call(['grep', '-i', 'cloudminds', MBN_FILE2])
    print MBN_FILE1 + ' secure: ' + str(out1 == 0)
    print MBN_FILE2 + ' secure: ' + str(out2 == 0)
    return out1 == 0 and out2 == 0


def add_item(root, name, text):
    item = ET.SubElement(root, "item")
    item.set("name", name)
    item.text = text.decode('utf-8')


def get_ota_package_name():
    for f in os.listdir(PRODUCT_OUT_DIR):
        if f.startswith(PRODUCT_NAME + '-ota'):
            return f


def generate_info_xml():
    package_info = ET.Element("PackageInfo")
    package_info.set("version", INFO_FILE_VERSION)

    print 'Reading properties...'
    info = read_properties(BUILD_PROP)
    for k in info:
        add_item(package_info, k, info[k])

    print 'Checking secure...'
    add_item(package_info, NAME_SECURE, '1' if is_secure() else '0')

    print 'Reading release note...'
    if os.path.exists(RELEASE_NOTE):
        with open(RELEASE_NOTE) as note:
            text = ''
            for line in note:
                text += line
            add_item(package_info, NAME_RELEASE_NOTE, text)
    else:
        print 'Warning: ' + RELEASE_NOTE + ' is NOT Found!'

    print 'Writing info file...'
    with open(INFO_XML, 'w') as xml:
        tree = ET.ElementTree(package_info)
        tree.write(xml, encoding='utf-8', xml_declaration=True)


def generate_ota_plus_info_package():
    ota_package = os.path.join(PRODUCT_OUT_DIR, get_ota_package_name())
    ota_plus_package_temp = os.path.join(PRODUCT_OUT_DIR, "ota_temp.zip")

    with zipfile.ZipFile(ota_plus_package_temp, 'w') as z:
        z.write(ota_package, os.path.basename(ota_package))
        z.write(INFO_XML, os.path.basename(INFO_XML))

    os.rename(ota_package, OTA_PACKAGE_BACKUP)
    os.rename(ota_plus_package_temp, ota_package)


def main():
    print '###### Make OTA Plus Info Package start ######'
    print 'Generating info file...'
    generate_info_xml()
    print 'Generating package...'
    generate_ota_plus_info_package()
    print '###### Make OTA Plus Info Package end ######'


if __name__ == '__main__':
    main()
