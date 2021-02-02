#!/bin/bash

# RUN inside container (~5 hours runtime)

TIMEFORMAT="%R"
mkdir filtlong_filt nanoq_filt nanofilt_filt nanostat_stats nanoq_stats

for i in $(seq 1 100); do

    echo "Replicate: $i"

    echo "Nanoq stats"

    # test file stat nanoq
    (/usr/bin/time -v cat test.fq | nanoq) 2> nanoq_stats/${i}_nanoq_fq_stat
    # test file gzipped stat nanoq
    (/usr/bin/time -v cat test.fq.gz | nanoq) 2> nanoq_stats/${i}_nanoq_gz_stat

    echo "Nanostat stats"

    # test file stat nanostat 4 cpu
    (/usr/bin/time -v NanoStat --fastq test.fq -t 4) 2> nanostat_stats/${i}_nanostat_fq_stat
    # test file stat gzipped nanostat 4 cpu
    (/usr/bin/time -v NanoStat --fastq test.fq.gz -t 4) 2> nanostat_stats/${i}_nanostat_gz_stat

    echo "Nanofilt filters"

    # test file filt nanofilt
    (/usr/bin/time -v cat test.fq | NanoFilt -l 5000 > /dev/null) 2> nanofilt_filt/${i}_nanofilt_fq_filt
    # test file filt gzipped nanofilt
    (/usr/bin/time -v zcat test.fq.gz | NanoFilt -l 5000 > /dev/null) 2> nanofilt_filt/${i}_nanofilt_gz_filt

    echo "Nanoq filters"

    # test file filt nanoq
    (/usr/bin/time -v cat test.fq | nanoq -l 5000 > /dev/null) 2> nanoq_filt/${i}_nanoq_fq_filt
    # test file filt gzipped nanoq
    (/usr/bin/time -v cat test.fq.gz | nanoq -l 5000 > /dev/null) 2> nanoq_filt/${i}_nanoq_gz_filt

    echo "Filtlong filters"

     # test file filt filtlong
    (/usr/bin/time -v filtlong --min_length 5000 test.fq > /dev/null) 2> filtlong_filt/${i}_filtlong_fq_filt
    # test file filt gzipped filtlong
    (/usr/bin/time -v filtlong --min_length 5000 test.fq.gz > /dev/null) 2> filtlong_filt/${i}_filtlong_gz_filt

done

mkdir replicate_benchmarks
mv filtlong_filt nanoq_filt nanofilt_filt nanostat_stats nanoq_stats ./replicate_benchmarks