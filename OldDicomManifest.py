#!/home/dariusmb/vene-mine/bin/python
from collections import defaultdict
from os import listdir
from os.path import isfile, join
import pandas as pd
import pydicom
import multiprocessing
import os
import SimpleITK as sitk
import sys

def main():
    if len(sys.argv) < 2:
        print("usage: OldDicomManifest.py inputDirectory outputFile")
        return
    inputDirectory = sys.argv[1]
    outputfile = sys.argv[2]
    dict = {}
    dicom_reader = sitk.ImageSeriesReader()
    dicom_file_names = dicom_reader.GetGDCMSeriesFileNames(inputDirectory)
    for i in dicom_file_names:
        f = str.split(i, "/")[8]
        ds = pydicom.read_file(i)
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
        dict.update({f: INList})
    mani = pd.DataFrame.from_dict(dict,
                                  orient='index',
                                  columns=['PatientID', 'SeriesDescription', 'StudyInstanceUID',
                                           'SeriesInstanceUID', 'StudyDate', 'Manufacturer', 'ManufacturerModelName',
                                           'SliceThickness', 'ReconstructionDiameter', 'ConvolutionKernel'])
    maniF = open(outputfile, 'w')
    mani.to_csv(maniF, header=True, sep=',')
    maniF.close()

if __name__ == "__main__":
      main()

# tempFiles = []
#
# rootdir = '/mnt/efs-new/copdgene/COPDgene_batch_01/COPDGene_A01751_COPDGene_A01751/'
# #rootdir = sys.argv[1]
# #rootdir = '/mnt/efs-new/copdgene/'
# for subdir, dirs, files in os.walk(rootdir):
#     for file in files:
#         if file.endswith(".dcm"):
#             tempFiles.append(os.path.join(subdir, file))
#
#
#
# #onlyfiles = [f for f in listdir(mypath_SHARP) if isfile(join(mypath_SHARP, f))]
# onlyfiles = tempFiles
# mydict2 = {}
# for file in onlyfiles:
#     #print(file)
#     f = str.split(file, "/")[8]
#     #filefull = [mypath_SHARP,file]
#     # #filefull = "".join(filefull)
#     ds = pydicom.read_file(file)
#     PatientID = ds.PatientID
#     SeriesDescription = ds.SeriesDescription
#     StudyInstanceUID = ds.StudyInstanceUID
#     SeriesInstanceUID = ds.SeriesInstanceUID
#     StudyDate = ds.StudyDate
#     Manufacturer = ds.Manufacturer
#     ManufacturerModelName = ds.ManufacturerModelName
#     SliceThickness = ds.SliceThickness
#     ReconstructionDiameter = ds.ReconstructionDiameter
#     ConvolutionKernel = ds.ConvolutionKernel
#     INList = [PatientID, SeriesDescription, StudyInstanceUID,
#               SeriesInstanceUID, StudyDate, Manufacturer, ManufacturerModelName,
#               SliceThickness, ReconstructionDiameter, ConvolutionKernel]
#     mydict2.update({f: INList})
#
# mani = pd.DataFrame.from_dict(mydict2,
#                               orient='index',
#                               columns=['PatientID', 'SeriesDescription', 'StudyInstanceUID',
#                                        'SeriesInstanceUID', 'StudyDate', 'Manufacturer', 'ManufacturerModelName',
#                                        'SliceThickness', 'ReconstructionDiameter', 'ConvolutionKernel'])
#
# maniF = open('COPDGeneDicomManifest_Full.txt', 'w')
# mani.to_csv(maniF, header=True, sep=',')
# maniF.close()

