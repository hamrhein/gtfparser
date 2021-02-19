#!/usr/bin/env python3

import argparse
import sys

import gtfparse


class TranscriptGeneMapException(Exception):
    pass


def main(args):
    instream = sys.stdin
    outstream = sys.stdout

    gtf = gtfparse.GtfParse(instream)

    num_transcripts_found = 0

    for gi in gtf:

        if gi["feature"] != "transcript":
            continue

        if num_transcripts_found == 0:
            if args.use_version:
                has_tv = args.transcript_vers_field in gi.attributes
                has_gv = args.gene_vers_field in gi.attributes

                if not has_tv & has_gv:
                    errstr = "Missing transcript version or gene version"
                    raise TranscriptGeneMapException(errstr)

            if not args.skip_gene_names:
                has_gn = args.gene_name_field in gi.attributes

                if not has_gn:
                    errstr = "Missing gene name field"
                    raise TranscriptGeneMapException(errstr)

        gid = gi.gene_id
        tid = gi.transcript_id

        if args.use_version:
            tid = "{}.{}".format(tid, gi.attributes[args.transcript_vers_field])
            gid = "{}.{}".format(gid, gi.attributes[args.gene_vers_field])

        if args.skip_gene_names:
            print(tid, gid, sep="\t", file=outstream)
        else:
            print(tid, gid, gi.attributes[args.gene_name_field], sep="\t",
                    file=outstream)

        num_transcripts_found += 1

    if num_transcripts_found == 0:
        errstr = "No transcripts found"
        raise TranscriptGeneMapException(errstr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True,
            description = "Creates transcript to gene info from GTF files. "
            "Reads from standard input and writes to standard output"""
            )

    parser.add_argument("--use_version", "-v", action="store_true",
            default=False, help="Use version numbers in transcript and gene IDs"
            )

    parser.add_argument("--skip_gene_names", "-s", action="store_true",
            default=False, help="Do not output gene names"
            )

    parser.add_argument("--transcript_vers_field", "-t",
            default="transcript_version",
            help="Field holding transcript version"
            )

    parser.add_argument("--gene_vers_field", "-g",
            default="gene_version", help="Field holding gene version"
            )

    parser.add_argument("--gene_name_field", "-n",
            default="gene_name", help="Field holding gene name"
            )

    args = parser.parse_args()

    main(args)
