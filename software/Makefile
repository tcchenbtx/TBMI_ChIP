# install required software:

install:
	# install trim_galore
	wget http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.5.zip
	unzip fastqc_v0.11.5.zip
	cd FastQC && chmod 755 fastqc
	pip install cutadapt
	wget http://www.bioinformatics.babraham.ac.uk/projects/trim_galore/trim_galore_v0.4.1.zip
	unzip trim_galore_v0.4.1.zip
	rm trim_galore_v0.4.1.zip
	# construct PATH
	echo Edit by TBMU_ChIP: >> ~/.profile
	echo export PATH=$(PATH):${CURDIR}/FastQC:${CURDIR}/trim_galore_zip:${CURDIR}/bowtie2-2.2.9:${CURDIR}/samtools-1.3.1:${CURDIR}/idrCode:${CURDIR}/meme/bin:${CURDIR}/Homer/.//bin/ >> ~/.profile
	source ~/.profile
	# Trim_galore for Mac user
	cd trim_galore_zip && sed 's/zcat/gzcat/g' trim_galore > mac_trim_galore
	cd trim_galore_zip && chmod 755 mac_trim_galore
	# install Bowtie2
	wget https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.2.9/bowtie2-2.2.9-source.zip/download
	unzip download
	rm download
	cd bowtie2-2.2.9 && make
	# install samtools
	wget https://github.com/samtools/samtools/releases/download/1.3.1/samtools-1.3.1.tar.bz2
	bzip2 -d samtools-1.3.1.tar.bz2
	tar -xvf samtools-1.3.1.tar
	cd samtools-1.3.1 && ./configure
	# install macs2
	pip install MACS2
	# install IDR
	wget https://sites.google.com/site/anshulkundaje/projects/idr/idrCode.tar.gz?attredirects=0
	mv idrCode.tar.gz?attredirects=0 idrCode.tar.gz 
	gzip -d idrCode.tar.gz
	tar -xvf idrCode.tar
	# install MEME_ChIP
	wget http://meme-suite.org/meme-software/4.11.2/meme_4.11.2_1.tar.gz
	tar zxf meme_4.11.2_1.tar.gz 
	cd meme_4.11.2 && ./configure --prefix=${CURDIR}/meme --with-url=http://meme-suite.org --enable-build-libxml2 --enable-build-libxslt 
	cd meme_4.11.2 && make && make test && make install
	cd ./meme/db/ && wget http://meme-suite.org/meme-software/Databases/motifs/motif_databases.12.12.tgz && tar -xvzf motif_databases.12.12.tgz

# install Homer two steps
homer_1:
	mkdir Homer
	cd Homer && wget http://homer.salk.edu/homer/configureHomer.pl
	cd bin && python Homer_genome.py
	
homer_2:
	cd Homer && perl configureHomer.pl -install mm10

# construct PATH
TBMI_path:
	echo Edit by TBMU_ChIP: >> ~/.profile
	echo export PATH=$(PATH):${CURDIR}/FastQC:${CURDIR}/trim_galore_zip:${CURDIR}/bowtie2-2.2.9:${CURDIR}/samtools-1.3.1:${CURDIR}/idrCode:${CURDIR}/meme/bin:${CURDIR}/Homer/.//bin/ >> ~/.profile
	source ~/.profile 
