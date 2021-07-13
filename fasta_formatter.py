# originally from https://ndownloader.figshare.com/files/20306223
ORIGINAL_FASTA_PATH = "coala40.fa"
FASTA_PATH = "esm40.fa"

MOST_COMMON_DRUG_RES = [
    "TRIMETHOPRIM",
    "MACROLIDE",
    "MULTIDRUG",
    "QUINOLONE",
    "PHENICOL",
    "AMINOGLYCOSIDE",
    "TETRACYCLINE",
    "FOLATE-SYNTHESIS-INHABITOR",
    "GLYCOPEPTIDE",
    "BETA-LACTAM",
]


def get_better_id(line):
    seq_id = line.split("|")
    drug = seq_id[-1].replace("/", "_")  # so the names of each embedding file does not have '/' in it
    keep = drug in MOST_COMMON_DRUG_RES
    return f"{seq_id[0].split(' ')[0]}|{seq_id[1].split(' ')[0]}|{drug}", keep


def filter_rare_aa(line):
    sequence = ""
    for aa in line:
        # if not in the top 20 most frequent amino acids
        if aa not in "ACDEFGHIKLMNPQRSTVWY":
            aa = "X"
        sequence += aa
    return sequence


def main():
    last_header = ""
    with open(ORIGINAL_FASTA_PATH, "r") as in_file, open(FASTA_PATH, "w") as out_file:
        keep = True
        for line in in_file:
            line = line.strip()
            if line.startswith(">"):
                last_header, keep = get_better_id(line)
            elif keep:
                # facebook's sequence length limit
                if len(line) <= 1024:
                    out_file.write(last_header + "\n")
                    sequence = filter_rare_aa(line)
                    out_file.write(sequence + "\n")
                last_header = ""


if __name__ == "__main__":
    main()
