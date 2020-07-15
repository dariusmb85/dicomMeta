from collections import defaultdict
from sys import argv
from os import listdir
from os.path import isfile, join
import pandas as pd
import pydicom
import os

tempFiles = []

rootdir = '/mnt/efs-new/copdgene/COPDgene_batch_01/COPDGene_A01751_COPDGene_A01751/19000101/'
#rootdir = '/mnt/efs-new/copdgene/'
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith(".dcm"):
            tempFiles.append(os.path.join(subdir, file))

# onlyfiles = [f for f in listdir(mypath_SHARP) if isfile(join(mypath_SHARP, f))]
onlyfiles = tempFiles
mydict = {}
for file in onlyfiles:
    # print(file)
    f = str.split(file, "/")[8]
    # print(f)
    # filefull = [mypath_SHARP,file]
    # filefull = "".join(filefull)
    # print(filefull)
    ds = pydicom.read_file(file)
    # print(ds)
    PatientID = ds.PatientID
    SeriesDescription = ds.SeriesDescription
    StudyInstanceUID = ds.StudyInstanceUID
    SeriesInstanceUID = ds.SeriesInstanceUID
    StudyDate = ds.StudyDate
    Manufacturer = ds.Manufacturer
    ManufacturerModelName = ds.ManufacturerModelName
    SliceThickness = ds.SliceThickness
    ReconstructionDiameter = ds.ReconstructionDiameter
    ConvolutionKernel = ds.ConvolutionKernel
    INList = [PatientID, SeriesDescription, StudyInstanceUID,
              SeriesInstanceUID, StudyDate, Manufacturer, ManufacturerModelName,
              SliceThickness, ReconstructionDiameter, ConvolutionKernel]
    mydict.update({f: INList})

mani = pd.DataFrame.from_dict(mydict, orient='index', columns=['PatientID', 'SeriesDescription', 'StudyInstanceUID',
                                                               'SeriesInstanceUID', 'StudyDate', 'Manufacturer',
                                                               'ManufacturerModelName',
                                                               'SliceThickness', 'ReconstructionDiameter',
                                                               'ConvolutionKernel'])

maniF = open('COPDGeneDicomManifest_Full.txt', 'w')
mani.to_csv(maniF, header=True, sep=',')
maniF.close()
