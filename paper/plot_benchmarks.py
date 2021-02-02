#!/usr/bin/env python

import pandas
import seaborn
from pathlib import Path
from matplotlib import pyplot as plt

def main():

    data = read_data()\
    
    data['time'] = pandas.to_datetime(data['time'], format="%M:%S.%f")
    data['time'] = data['time'].dt.second + data['time'].dt.microsecond/1e6
    data['mem'] = data['mem'].apply(lambda x: int(x)/1000)

    print(data)

    # plot_data(data)

def read_data() -> pandas.DataFrame:

    walltime = "Elapsed (wall clock) time (h:mm:ss or m:ss): "
    memory = "Maximum resident set size (kbytes): "

    data = []
    for adir in Path('replicate_benchmarks').glob("*"):
        for f in adir.glob("*"):
            replicate, tool, ftype, mode = f.name.split("_")

            t = parse_time(f, grep_str=walltime)
            mem = parse_time(f, grep_str=memory) 

            data.append({
                'replicate': replicate,
                'tool': tool,
                'ftype': ftype,
                'mode': mode,
                'time': t,
                'mem': mem
            })

    return pandas.DataFrame(data)

def parse_time(file: Path, grep_str: str = ""):

    with file.open() as f:
        for line in f:
            content = line.strip()
            if content.startswith(grep_str):
                return content.replace(grep_str, '')
    
    return


def plot_data(data: pandas.DataFrame) -> None:

    fig, axes = plt.subplots(
        nrows=1, ncols=2, figsize=(
            2 * 7, 1 * 4.5
        )
    )

    data = data[data["ftype"] != "crab"]  # exlude bio parser for now, slightly slower than needletail

    for mode, _data in data.groupby("mode"):
        for tool, __data in _data.groupby("tool"):
            for ftype, ___data in __data.groupby("ftype"):
                mean_seconds = ___data['time'].mean()
                std_seconds = ___data['time'].std()
                print(f"Mode: {mode} Ftype: {ftype} - Tool: {tool} - Mean: {mean_seconds} - Standard Deviation: {std_seconds}")

    filter_data = data[data['mode'] == 'filt']
    stats_data = data[data['mode'] == 'stat']

    seaborn.barplot(
        y='time', x='ftype', hue='tool', data=filter_data,
        ax=axes[0], palette=["#E69F00", "#56B4E9", "#009E73"]
    )
    
    seaborn.barplot(
        y='time', x='ftype', hue='tool', data=stats_data,
        ax=axes[1], palette=["#E69F00", "#009E73"], hue_order=["nanostat", "nanoq"]
    )

    axes[0].set_xlabel("")
    axes[0].set_ylabel("seconds\n")
    axes[1].set_xlabel("")
    axes[1].set_ylabel("seconds\n")

    axes[0].title.set_text('Read filter (walltime)')
    axes[1].title.set_text('Read statistics (walltime)')

    plt.tight_layout()
    fig.savefig('benchmarks.png')

main()