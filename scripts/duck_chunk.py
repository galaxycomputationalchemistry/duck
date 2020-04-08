import argparse

try:
    from duck.steps.chunk import (
        chunk_with_amber,
        do_tleap,
        remove_prot_buffers_alt_locs,
        find_disulfides,
    )
except ModuleNotFoundError:
    print('Dependencies missing; check openmm, pdbfixer, and yank are installed from Omnia.')

def main():
    parser = argparse.ArgumentParser(description='Perform chunking in preparation for dynamic undocking')
    parser.add_argument('-p', '--protein', help='Apoprotein in PDB format')
    parser.add_argument('-l', '--ligand', help='Ligand in mol format')
    # parser.add_argument('-o', '--output', help="PDB output")
    parser.add_argument('-c', '--cutoff', type=float, help='Cutoff for chunk calculation')
    parser.add_argument('-b', '--ignore-buffers', action='store_true', help='Do not remove buffers (solvent, ions etc.)')
    parser.add_argument('-i', '--interaction', help='Protein atom to use for ligand interaction.')

    args = parser.parse_args()

    # A couple of file name
    orig_file = prot_file = args.protein
    chunk_protein = "protein_out.pdb"
    chunk_protein_prot = "protein_out_prot.pdb"
    # Do the removal of buffer mols and alt locs
    if not args.ignore_buffers:
        prot_file = remove_prot_buffers_alt_locs(prot_file)
    # Do the chunking and the protonation
    chunk_with_amber(
        args.ligand, prot_file, args.interaction, chunk_protein, args.cutoff, orig_file
    )
    # Protonate
    disulfides = find_disulfides(chunk_protein)
    do_tleap(chunk_protein, chunk_protein_prot, disulfides)
    

if __name__ == "__main__":
    main()
