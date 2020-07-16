#!/bin/bash

# Read in pipe output
dicom_stack=$1

# Substrings for changing current to save directories
dicom_batch="/mnt/efs-new/copdgene/COPDgene_batch_[0-9][0-9]"
manifest_dir="/mnt/efs-new/copdgene-manifest"

# Get directory, convert to output directory
# Does output directory exist?
# If no, create it
dir_path=$(dirname "${dicom_stack}")
if [[ ! -d "${dir_path/$dicom_batch/$manifest_dir}" ]]
then
	mkdir -p "${dir_path/$dicom_batch/$manifest_dir}"
fi

# Get output manifest file name
# Does it already exist?
# If yes, skip
manifest_name="${dicom_stack/$dicom_batch/$nrrd_dir}_mani.csv"
if [[ ! -f "${manifest_name}" ]]
then
	python /home/dariusmb/Git/dicomMeta/OldDicomManifest.py ${dicom_stack} ${manifest_name}
else
	echo "File ${manifest_name} already exists."
fi

