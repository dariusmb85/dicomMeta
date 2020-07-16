from collections import defaultdict
from sys import argv
from os import listdir
from os.path import isfile, join
import pandas as pd
import pydicom
import multiprocessing
import os

def GetMetaData(fileName, mydict):
    f = str.split(fileName,"/")[8]
    ds = pydicom.read_file(fileName)
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
    mydict[f] = INList
    return mydict



def parallelMetaData(arg):
    manager = multiprocessing.Manager()
    mydict = manager.dict()
    jobs = []
    #file = sys.argv[1]
    AllFiles = arg
    #ds = pydicom.read_file(file)
    for i in AllFiles:
        p = multiprocessing.Process(target=GetMetaData, args=(i, mydict))
        jobs.append(p)
        p.start()
    for proc in jobs:
        proc.join()
    return mydict


tempFiles = []

rootdir = '/mnt/efs-new/copdgene/COPDgene_batch_01/COPDGene_A01751_COPDGene_A01751/'
#rootdir = sys.argv[1]
#rootdir = '/mnt/efs-new/copdgene/'
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file.endswith(".dcm"):
            tempFiles.append(os.path.join(subdir, file))



# onlyfiles = [f for f in listdir(mypath_SHARP) if isfile(join(mypath_SHARP, f))]
#onlyfiles = tempFiles[0:9]
#mydict2 = {}

mydat = parallelMetaData(tempFiles)
mani = pd.DataFrame.from_dict(mydat,
                              orient='index',
                              columns=['PatientID', 'SeriesDescription', 'StudyInstanceUID',
                                       'SeriesInstanceUID', 'StudyDate', 'Manufacturer', 'ManufacturerModelName',
                                       'SliceThickness', 'ReconstructionDiameter', 'ConvolutionKernel'])

maniF = open('COPDGeneDicomManifest_Full.txt', 'w')
mani.to_csv(maniF, header=True, sep=',')
maniF.close()
