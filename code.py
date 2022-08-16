import yaml
import sys
import json
import shutil
import logging
import wget 
import os
import tarfile

def Create_JSON_File(text,file):
    with open(file, 'w') as json_file:
        json.dump(text, json_file, indent=4)
    logging.info('JSON file created!')

def Create_Release_Notes_File(text,file):
    with open(file, 'w') as f:
        for (key, values) in text.items():
            f.write('\n%s:\n' % key)
            if isinstance(values, list):
                for value in values:
                    f.write('%s:\n' % value)
            else:
                f.write('%s:\n' % value)
    logging.info('Release notes file created!')
def Find_RPM_Files(file,rpm):
    try: 
        f = open(file)      
        data = json.load(f)
        for values in data['CESA_list']:
            for (key, value) in values.items():
                if key == 'RPM_list':
                    for (key2, value2) in value.items():
                        if key2 == 'rpm_pkg':
                             rpm.append(value2)    
    except:
        logging.error("File (%s) doesnt exist!" %(file))
def Download_Packages(rpm,url,directory):
    if len(rpm) > 0:    
        for file in rpm: 
            wget.download(url+file,os.path.join(directory,file))
        logging.info('RPM files downloaded!')	
    else:
        logging.warning('No RPM files to download!')
def make_tarfile(tarball,directory):
    try:
        with tarfile.open(tarball, "w:gz") as tar:
            tar.add(directory, arcname=os.path.basename(directory))
        logging.info('tarball created!')
    except:
        logging.error('Directory to be compressed doesn\'t exist!')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs.log",'w+'),
        logging.StreamHandler(sys.stdout)
    ]
)
rpm = []
directory = 'files'
url = 'http://mirror.centos.org/centos/7/os/x86_64/Packages/'
tarball = 'CVM_PE_GI-7.7r1.6.1-20200303-x86_64.tar.gz'
JSON_file = os.path.join(directory,'CVM_RPM_LIST_MANIFEST.json')
Release_notes_file = os.path.join(directory,'CVM_PE_GI-7.7r1.7.1-20200319-x86_64.release_note')
YamlFile = 'data.yaml'
try:
    logging.info('Making a new directory to store JSON file, Release notes file and RPM packages...')
    os.mkdir(directory)
except:
    logging.error('Directory already exists!')
    input1 =  input('Do you want to overwrite the the existing directory? y/n:  '  )
    if input1 == 'y':
        shutil.rmtree(directory)
        os.mkdir(directory)		
else: 
    logging.info('New Directory created!')

logging.info('Opening the YAML file...')

try:
    with open(YamlFile, 'r') as file:
        logging.info('YAML file opened!')
        logging.info('Reading YAML file...')
        configuration = yaml.safe_load(file)
except:
    logging.error('YAML file doesnt exist!')

else:
    logging.info('Creating a JSON file...')
    Create_JSON_File(configuration['JSON'],JSON_file)
    logging.info('Creating a Release notes file...')
    Create_Release_Notes_File(configuration['RELEASE_NOTE'],Release_notes_file)
    logging.info('Looking for RPM files to download...')
    Find_RPM_Files(JSON_file, rpm)
    logging.info('Downloading RPM files...')
    Download_Packages(rpm,url,directory)
    logging.info('Creating a tarball...')	
    make_tarfile(tarball,directory)

