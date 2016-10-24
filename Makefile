# configure the system:
Mac_User:
	/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	brew install wget
	brew install coreutils gnu-sed

# configure based on user input:
configure:
	cd bin && python check_config.py

# install required softwares:
install_software:
	cd software && make install
	cd software && make homer_1
	cd software && make homer_2
	cd software && make TBMI_path

# run TrimGalore
T:
	cd bin && python read_configure.py
	cd bin && make TrimGalore

# run Bowtie2
B:
	cd bin && python read_trimgalore.py
	cd bin && make reference
	cd bin && make bowtie2

# run MACS2
M:
	cd bin && python get_BAM.py
	cd bin && make get_BAM
	cd bin && make merge
	cd bin && python go_macs2.py
	cd bin && make macs2

# run IDR
I:
	cd bin && python go_clean_before_IDR.py
	cd bin && make clean_up
	cd bin && python go_IDR.py
	cd bin && make IDR

# run MEME-ChIP
motif:
	cd bin && python go_meme.py
	cd bin && make meme_1
	cd bin && make meme_2
	cd bin && make meme_3

# run Homer
annotation:
	cd bin && python go_homer.py
	cd bin && make Homer_annotation


# run ALL
All:
	cd bin && python read_configure.py
	cd bin && make TrimGalore
	cd bin && python read_trimgalore.py
	cd bin && make reference
	cd bin && make bowtie2
	cd bin && python get_BAM.py
	cd bin && make get_BAM
	cd bin && make merge
	cd bin && python go_macs2.py
	cd bin && make macs2
	cd bin && python go_clean_before_IDR.py
	cd bin && make clean_up
	cd bin && python go_IDR.py
	cd bin && make IDR
	cd bin && python go_meme.py
	cd bin && make meme_1
	cd bin && make meme_2
	cd bin && make meme_3
	cd bin && python go_homer.py
	cd bin && make Homer_annotation

# clean_up_output
Clean_My_Output:
	cd bin && rm file_list.txt pair_file_path.json pair_list.json process_files.txt userinput.json *.pyc
	rm -r output
	mkdir output

Uninstall_Software:
	cd software && rm -r FastQC
	cd software && rm -r Homer
	cd software && rm -r bowtie2-2.2.9
	cd software && rm -r idrCode
	cd software && rm -r meme
	cd software && rm -r meme_4.11.2
	cd software && rm -r samtools-1.3.1
	cd software && rm fastqc_* idrCode.tar meme* samtools*


Delete_My_Dataset:
	rm -r dataset
	mkdir dataset
	
