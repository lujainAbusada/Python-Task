import yaml
import json
import logging
import wget 
import os
import tarfile

def Create_JSON_File(text,file):
    with open(file, 'w') as json_file:
        json.dump(text, json_file, indent=4)


def Create_Release_Notes_File(text,file):
    with open(file, 'w'
              ) as f:
        for (key, values) in text.items():
            f.write('\n%s:\n' % key)
            if isinstance(values, list):
                for value in values:
                    f.write('%s:\n' % value)
            else:
                f.write('%s:\n' % value)

def Find_RPM_Files(file,rpm):
    f = open(file)      
    data = json.load(f)
    for values in data['CESA_list']:
        for (key, value) in values.items():
            if key == 'RPM_list':
                for (key2, value2) in value.items():
                    if key2 == 'rpm_pkg':
                         rpm.append(value2)    


def Download_Packages(rpm,url,directory):
    for file in rpm: 
        wget.download(url+file,os.path.join(directory,file))	

def make_tarfile(tarball,directory):
    with tarfile.open(tarball, "w:gz") as tar:
        tar.add(directory, arcname=os.path.basename(directory))

rpm = []
directory = 'files'
url = 'http://mirror.centos.org/centos/7/os/x86_64/Packages/'
tarball = 'CVM_PE_GI-7.7r1.6.1-20200303-x86_64.tar.gz'
JSON_file = os.path.join(directory,'CVM_RPM_LIST_MANIFEST.json')
Release_notes_file = os.path.join(directory,'CVM_PE_GI-7.7r1.7.1-20200319-x86_64.release_note')
YamlFile = 'data.yaml'

if os.path.isdir(directory) == False:
    os.mkdir(directory)

with open(YamlFile, 'r') as file:
    configuration = yaml.safe_load(file)

Create_JSON_File(configuration['JSON'],JSON_file)
Create_Release_Notes_File(configuration['RELEASE_NOTE'],Release_notes_file)
Find_RPM_Files(JSON_file, rpm)
Download_Packages(rpm,url,directory)
make_tarfile(tarball,directory)
