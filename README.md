# TBMI_ChIP
TBMI_ChIP pipeline

![alt tag](https://github.com/tcchenbtx/TBMI_ChIP/blob/master/overview.png)

## Dependencies:
The dependencies for the following software should be installed first:
TrimGalore, FastQC, Bowtie2, MACS2, IDR, MEME-ChIP, Homer

## What the TBMI_ChIP can help:

This TBMI_ChIP can help to perform the follwing:
1. Use TrimGalore to trim your data
2. Use FastQC to check the quality of your trimmed dataset
3. Use Bowtie2 to align your sequencing results
4. After Bowtie2, the dataset will be merged and sorted then converted to BAM files for peak calling
5. Use MACS2 to call peak based on your setting
6. Run IDR to study the consistency of your ChIP-seq data
7. Run MEME-ChIP to perform motif analysis
8. Run Homer for gene annotation.

## How to use TBMI_ChIP:
1. Put your ChIP-seq data under dataset folder
2. modify the configure/configure.txt based on instructions
3. in the main folder, use the following command to use the TBMI_ChIP:
  1. <code>make configure</code> : to read through your configure input
  2. <code>make install_software</code>: install necessary software (this step can be skipped if you install necessary software mannually)
  3. <code>make T</code> : run TrimGalore to trim your data
  4. <code>make B</code> : run Bowtiew2 to sequence alignment
  5. <code>make M</code> : run MACS2 for peak calling
  6. <code>make I</code> : run IDR for consistency analysis
  7. <code>make motif</code>: run MEME-ChIP for motif analysis
  8. <code>make annotation</code> : run Homer for gene annotation

### Short cut:
You can also go through all analysis with the following commands:
  1. <code>make configure</code> : to read through your configure input                      
  2. <code>make install_software</code> : install necessary software (this step can be skipped if you install necessary software mannually)
  3. <code>make All</code>

## Other helpful commands:
* <code>make Clean_My_Output</code> : clean up the output folder
* <code>make Uninstall_Software</code> : uninstall software
* <code>make Delete_My_Dataset</code> : (please use with care) clean up the dataset folder



