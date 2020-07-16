#!/bin/bash
#Edited from Matt Satusky script

for dicom_dir in $(find /mnt/efs-new/copdgene -mindepth 1 -maxdepth 1 -type d -name "COPDgene_batch*")
do
        time echo "$(readlink -f $(find ${dicom_dir} -mindepth 2 -type d -name "*SHARP*" -or -iname "*B35f"))" |  parallel /home/dariusmb/Git/dicomMeta/dicom_make_Manifest.sh {}
        wait
        echo "$(basename $dicom_dir) done."
done