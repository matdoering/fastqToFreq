# fastqToFreq
Uses [MinVar](https://github.com/ozagordi/MinVar) and [bamToFreq](https://github.com/matdoering/bamToFreq) to convert next-generation sequencing reads (fastq/fastq.gz) to frequency files (csv).

## Usage
This program is intended for use via Docker only. It can be used in the following way:
```
docker run -v <bamFolder>:/data/ mdoering88/fastqtofreq:latest /data/

```
or via an interactive session

```
docker run -v <bamFolder>:/data/ -it --entrypoint /bin/bash mdoering88/fastqtofreq:latest
```

and then calling ```run_minvar.sh```, ```minvar```, or ```bamToFreq``` for custom processing.

## Limitations
- Only single-end sequencing reads are supported (use R1 file in case of paired-end data)
- The number of reads is downsampled to speed up the computations
- Only resistant-relevant regions of HIV-1 and HCV are supported


