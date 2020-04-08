import argparse
import pickle

try:
    from duck.steps.parametrize import prepare_system
    from duck.utils.cal_ints import find_interaction
    from duck.steps.equlibrate import do_equlibrate
    from duck.utils.check_system import check_if_equlibrated
except ModuleNotFoundError:
    print('Dependencies missing; check openmm, pdbfixer, and yank are installed from Omnia.')

def main():
    parser = argparse.ArgumentParser(description='Prepare system for dynamic undocking')
    parser.add_argument('-p', '--protein', help='Apoprotein in PDB format')
    parser.add_argument('-l', '--ligand', help='Ligand in mol format')
    # parser.add_argument('-o', '--output', help="PDB output")
    parser.add_argument('-c', '--chunk', help='Chunked protein')
    parser.add_argument('-i', '--interaction', help='Protein atom to use for ligand interaction.')
    parser.add_argument('-s', '--seed', type=int, help='Random seed.')
    parser.add_argument('--gpu-id', type=int, help='GPU ID (optional); if not specified, runs on CPU only.')
    parser.add_argument('--force-constant-eq', type=float, default=1.0, help='Force constant for equilibration.')

    args = parser.parse_args()
    # Parameterize the ligand

    prepare_system(args.ligand, args.chunk)
    # Now find the interaction and save to a file
    results = find_interaction(args.interaction, args.protein)
    print(results) # what happens to these?
    with open('complex_system.pickle', 'rb') as f:
        p = pickle.load(f) + results
    with open('complex_system.pickle', 'wb') as f:
        pickle.dump(p, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    #     pickle.dump(l, 'complex_system.pickle')
    # Now do the equlibration
    do_equlibrate(force_constant_equilibrate=args.force_constant_eq, gpu_id=args.gpu_id)
    if not check_if_equlibrated("density.csv", 1):
        raise EquilibrationError("System is not equilibrated.")

if __name__ == "__main__":
    main()
