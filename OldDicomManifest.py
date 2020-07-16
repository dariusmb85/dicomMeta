#!/home/dariusmb/vene-mine/bin/python
from collections import defaultdict
from os.path import isfile, join
import pandas as pd
import pydicom
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
