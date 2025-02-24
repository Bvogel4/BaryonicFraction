import pynbody
import numpy as np
import pandas as pd
from pathlib import Path
import pymp
import os
import re
from glob import glob

from scipy import stats
import traceback


def find_simulation_snapshots(sim_path):
    """
    Find all available snapshots for a given simulation.

    Parameters:
    sim_path: path to a specific simulation snapshot (used to determine pattern)

    Returns:
    list: Sorted list of snapshot paths
    """
    # Parse the simulation name and base path
    sim_path = Path(sim_path)
    base_path = sim_path.parent.parent.parent
    sim_name = sim_path.name.split('.')[
        0]  # Get the simulation name (e.g., 'cptmarvel')
    print(f"Base path: {base_path}, Simulation name: {sim_name}")

    # Build the pattern for finding snapshots
    # Pattern will match only files ending in 6 digits
    snapshot_pattern = f"{base_path}/{sim_name}.cosmo*/**/ahf_200/{sim_name}.cosmo*.[0-9][0-9][0-9][0-9][0-9][0-9]"  # to make this more general pass this as an argument

    # Find all matching snapshots
    snapshot_paths = glob(snapshot_pattern, recursive=True)

    # Filter out any matches that aren't just numbers at the end
    snapshot_paths = [path for path in snapshot_paths if
                      re.search(r'\.\d{6}$', path)]

    # Extract step numbers and create (step, path) pairs
    snapshot_info = []
    for path in snapshot_paths:
        try:
            # Extract the step number from the path
            step = int(re.search(r'\.(\d{6})$', path).group(1))
            snapshot_info.append((step, path))
        except (ValueError, IndexError, AttributeError):
            print(f"Warning: Could not parse step number from {path}")
            continue

    # Sort by step number in descending order (newest first)
    snapshot_info.sort(reverse=True)

    steps = [step for step, _ in snapshot_info]
    step_diffs = np.diff(steps)
    # print(f"Snapshot step differences: {step_diffs}")

    # check if the each step has a corresponding '.iord' file, if not, remove it from the list
    for step, path in snapshot_info:
        iord_file = f"{path}.iord"
        if not os.path.exists(iord_file):
            print(f'{iord_file} does not exist')
            print(f'removing {path} from list')
            snapshot_info.remove((step, path))
        # also check for .param file
        param_file = f"{path}.param"
        if not os.path.exists(param_file):
            print(f'{param_file} does not exist')
            full_sim_name = base_path.name
            #try and read it from sim level param file
            sim_param_file = f"{base_path}/{full_sim_name}.param"
            if not os.path.exists(sim_param_file):
                #print(f"Warning: Missing .param file for snapshot {step}")
                print(f'{sim_param_file} does not exist')
                snapshot_info.remove((step, path))
            #if it does exist create a symlink to it
            else:
                print(f"Creating symlink to sim level param file for snapshot {step}")
                os.symlink(sim_param_file,param_file)

    # print mode of step_diffs
    mode = stats.mode(step_diffs)[0]
    print(f"Most common step difference: {mode}")

    # if sim_name in ['cptmarvel']:
    #     # use only snapshots that are 128 steps apart
    #     snapshot_info = [info for info in snapshot_info if info[0] % mode == 0]
    #     steps = [step for step, _ in snapshot_info]
    #     step_diffs = np.diff(steps)
    #     print(f"Snapshot step differences: {step_diffs}")
    #
    # if sim_name in ['h229','h242','h329']:
    # use only snapshots that are multples of 32 apart, eg 64,96,128
    snapshot_info = [info for info in snapshot_info if info[0] % 32 == 0]
    print(
        f"Using {len(snapshot_info)} snapshots with step difference 32")

    steps = [step for step, _ in snapshot_info]
    step_diffs = np.diff(steps)
    print(f"Snapshot step differences: {step_diffs}")
    

    # Return the sorted paths
    return [path for _, path in snapshot_info]


def find_simulation_directories(base_path, pattern="*cosmo*.4096*"):
    """
    Find all simulation directories that contain valid simulation snapshots.

    Parameters:
    base_path: Base directory to search
    pattern: Basic pattern to match simulation directories

    Returns:
    list: List of valid simulation directories
    """
    base_path = Path(base_path)
    valid_sim_dirs = []

    # First find candidate directories
    candidate_dirs = list(base_path.glob(pattern))

    for sim_dir in candidate_dirs:
        # Look for snapshot files that end in exactly 6 digits
        snapshot_pattern = f"{sim_dir}/**/ahf_200/*.??????"
        snapshots = glob(snapshot_pattern, recursive=True)

        # Filter for valid simulation files (ending in 6 digits without extensions)
        valid_snapshots = [snap for snap in snapshots
                           if re.search(r'\.\d{6}$', snap)
                           and not any(snap.endswith(ext) for ext in
                                       ['.parameter', '.param', '.kdtree',
                                        '.info'])]

        if valid_snapshots:
            valid_sim_dirs.append(sim_dir)

    return valid_sim_dirs


def find_matching_halos(final_halo, progenitor_halos):
    """Track particle relationships between a final halo and its potential progenitors"""
    matching_halos = {
        final_halo.properties['halo_number']: {
            'progenitors': {},
            'total_particles': len(final_halo['iord'])
        }
    }

    final_iords = final_halo['iord']
    final_count = len(final_iords)

    for progenitor_halo in progenitor_halos:
        progenitor_iords = progenitor_halo['iord']
        progenitor_count = len(progenitor_iords)
        matching_iords = np.intersect1d(final_iords, progenitor_iords)
        match_count = len(matching_iords)

        if match_count > 0:
            percent_in_final = (
                                           match_count / final_count) * 100  # What fraction of final halo came from this progenitor
            percent_of_progenitor = (
                                                match_count / progenitor_count) * 100  # What fraction of progenitor ended up in final
            #
            # #print what is going on in bizzare case where percent_in_final is close to 100 but percent_of_progenitor is low
            # if percent_in_final > 95 and percent_of_progenitor < 5:
            #     print(f"WARNING: Suspicious match detected in final halo {final_halo.properties['halo_number']} - progenitor {progenitor_halo.properties['halo_number']}")
            #     print(f"  - Percent in final: {percent_in_final:.1f}%", f"  - Percent of progenitor: {percent_of_progenitor:.1f}%")
            #     print(f'match count: {match_count}, final count: {final_count}, progenitor count: {progenitor_count}')
            #

            matching_halos[final_halo.properties['halo_number']]['progenitors'][
                progenitor_halo.properties['halo_number']] = {
                'matching_particles': match_count,
                'percent_in_final': percent_in_final,
                'percent_of_progenitor': percent_of_progenitor,
                'Mvir': progenitor_halo.properties['Mvir'],
                'n_star': progenitor_halo.properties['n_star'],
                'npart': progenitor_halo.properties['npart'],
                'total_particles': progenitor_count
            }

    return matching_halos


def validate_snapshot_data(halos_with_stars, merger_histories, step):
    """
    Validate that all halos were properly processed and stored.

    Parameters:
    halos_with_stars: list of halos that should have been processed
    merger_histories: dictionary of processed halo data
    step: current snapshot step number for error reporting

    Returns:
    bool: True if validation passes, raises exception if validation fails
    """
    # Get all halo IDs that should have been processed
    expected_halo_ids = {halo.properties['halo_number'] for halo in
                         halos_with_stars}

    # Get all halo IDs that were actually processed
    processed_halo_ids = set(merger_histories.keys())

    # Check for missing halos
    missing_halos = expected_halo_ids - processed_halo_ids
    if missing_halos:
        raise ValueError(
            f"Snapshot {step} is missing data for halos: {missing_halos}")

    # Check for extra halos (shouldn't happen, but good to check)
    extra_halos = processed_halo_ids - expected_halo_ids
    if extra_halos:
        raise ValueError(
            f"Snapshot {step} has unexpected extra halos: {extra_halos}")

    return True


def validate_progenitor_match(percent_in_final, percent_of_progenitor,
                              threshold=20):
    """
    Validate if a progenitor match is physically meaningful.
    """
    if percent_in_final > 100 - threshold and percent_of_progenitor > 100 - threshold:
        return "main progenitor"
    elif percent_in_final < threshold and percent_of_progenitor < threshold:
        return "exchange"
    # Split: Most/all of final halo came from small piece of progenitor
    elif percent_in_final > 80 and percent_of_progenitor < 20:
        return "split"
    # Merger: Most of progenitor ends up in final but is small part of it
    elif percent_in_final < 50 and percent_of_progenitor > 50:
        return "merger"
    else:
        return "unknown"


def filter_progenitors(progenitors, threshold=50.0):
    """
    Calculate total mass only from progenitors that contribute significantly.

    Parameters:
    progenitors: dict of progenitor information
    threshold: minimum percentage of progenitor that must end up in final halo

    Returns:
    tuple: (total_mass, filtered_ids, rejected_ids)
    """

    filtered_ids = []
    rejected_ids = []

    for prog_id, prog in progenitors.items():
        if prog[
            'percent_of_progenitor'] > threshold:  # only count progenitors where most of the particles end up in the final halo
            filtered_ids.append(prog_id)
        else:
            rejected_ids.append(prog_id)
    # return filtered progenitors, filtered ids, rejected ids
    filtered_progenitors = {prog_id: prog for prog_id, prog in
                            progenitors.items()
                            if prog_id in filtered_ids}

    return filtered_progenitors, filtered_ids, rejected_ids


def process_halo(halo, current_step, time, h, halo_id, halos_earlier_with_stars,
                 halos_earlier_dark, contribution_threshold):
    # Initialize enhanced halo data with more detailed merger info
    halo_data = {
        'final_state': {
            'mvir': halo.properties['Mvir'] / h,
            'm_star': halo.properties['M_star'] / h,
            'snapshot': current_step,
            'time': time,
            'n_star': halo.properties['n_star'],
        },
        'merger_info': {
            'has_merger': False,  # flag for merger event
            'dark_merger': None,  # flag for mergers that do not involve stars
            'merger_ratio': None,  # total merger ratio including dark halos
            'merger_ratio_stellar_only': None,
            # merger ratio with galaxies that have stars only
            'main_progenitor': None,  # main progenitor halo ID
            'main_progenitor_mvir': None,  # main progenitor virial mass
            'minor_stellar_mvir': 0,
            # mass from progenitors that have stars (excluding main)
            'total_minor_mvir': 0,
            # total mass from minor progenitors (with dark)
            'progenitors': [],
            # progenitors that met threshold (most particles in final halo)
            'dark_progenitors': [],  # dark halos that met threshold
            'rejected_minor_progenitors': [],  # progenitors below threshold
            'rejected_dark_progenitors': [],  # dark halos below threshold
            'contribution_threshold': contribution_threshold,
            # Store threshold used
        },
        'progenitor_details': {}
    }

    stellar_matches = find_matching_halos(halo, halos_earlier_with_stars)

    dark_matches = find_matching_halos(halo, halos_earlier_dark)

    halo_data['progenitor_details']['stellar'] = stellar_matches[halo_id][
        'progenitors']
    stellar_progenitors = stellar_matches[halo_id]['progenitors']

    halo_data['progenitor_details']['dark'] = dark_matches[halo_id][
        'progenitors']
    dark_progenitors = dark_matches[halo_id]['progenitors']

    main_prog_id = None
    main_prog_mvir = 0

    # filter progenitors and find main progenitor
    if stellar_progenitors:
        # filter out progenitors that contribute less than threshold
        stellar_progenitors, filtered_stellar_ids, rejected_stellar_ids = filter_progenitors(
            stellar_progenitors, contribution_threshold)
        if stellar_progenitors:
            main_prog_id = max(stellar_progenitors.items(),
                               key=lambda x: x[1]['Mvir'])[0]
            main_prog_mvir = stellar_progenitors[main_prog_id]['Mvir']
    else:
        if dark_progenitors:  # Only try to get dark progenitor if there are any
            main_prog_id = max(dark_progenitors.items(),
                               key=lambda x: x[1]['Mvir'])[0]
            main_prog_mvir = dark_progenitors[main_prog_id]['Mvir']
        filtered_stellar_ids = []
        rejected_stellar_ids = []

        # check if there is a more massive dark progenitor
    if dark_progenitors:
        dark_progenitors, filtered_dark_ids, rejected_dark_ids = filter_progenitors(
            halo_data['progenitor_details']['dark'],
            contribution_threshold
        )
        if dark_progenitors:
            dark_prog_id = max(dark_progenitors.items(),
                               key=lambda x: x[1]['Mvir'])[0]
            dark_mvir = dark_progenitors[dark_prog_id]['Mvir']

            # Update main progenitor if dark one is more massive

            if dark_mvir > main_prog_mvir:
                main_prog_id = dark_prog_id
                # only unusual if there is a stellar progenitor
                if stellar_progenitors:
                    print(
                        f'found dark progenitor more massive than main stellar progenitor for halo {halo_id} Dark Mvir: {dark_mvir}, Stellar Mvir: {main_prog_mvir}')
                main_prog_mvir = dark_mvir
    else:
        filtered_dark_ids = []
        rejected_dark_ids = []

    # Add safety check
    if main_prog_id is None:
        print(
            f"Warning: No main progenitor found for halo {halo_id} at snapshot {current_step}")

    # Validate matches
    for prog_id, prog in stellar_progenitors.items():
        match_type = validate_progenitor_match(
            prog['percent_in_final'],
            prog['percent_of_progenitor']
        )
        halo_data['progenitor_details']['stellar'][prog_id][
            'match_type'] = match_type
    for prog_id, prog in dark_progenitors.items():
        match_type = validate_progenitor_match(
            prog['percent_in_final'],
            prog['percent_of_progenitor']
        )
        halo_data['progenitor_details']['dark'][prog_id][
            'match_type'] = match_type

    n_prog = len(stellar_progenitors) + len(dark_progenitors)

    if (n_prog) > 1:  # merger event
        # Find main progenitor (highest Mvir)
        minor_stellar_mvir = 0
        minor_dark_mvir = 0
        if stellar_progenitors:
            minor_stellar_progenitors = {prog_id: prog for prog_id, prog in
                                         stellar_progenitors.items()
                                         if prog_id != main_prog_id}
            minor_stellar_mvir = sum(
                prog['Mvir'] for prog in minor_stellar_progenitors.values())
        else:
            minor_stellar_progenitors = {}
            minor_stellar_mvir = 0
        if dark_progenitors:
            minor_dark_progenitors = {prog_id: prog for prog_id, prog in
                                      dark_progenitors.items()
                                      if prog_id != main_prog_id}
            minor_dark_mvir = sum(
                prog['Mvir'] for prog in minor_dark_progenitors.values())
        else:
            minor_dark_progenitors = {}
            minor_dark_mvir = 0

        total_minor_mvir = minor_stellar_mvir + minor_dark_mvir

        if total_minor_mvir > 0:
            total_ratio = main_prog_mvir / total_minor_mvir

            if minor_stellar_mvir > 0:
                stellar_ratio = main_prog_mvir / minor_stellar_mvir
                has_dark_merger = False
            else:
                stellar_ratio = None
                has_dark_merger = minor_dark_mvir > 0
                # Update all merger information
            halo_data['merger_info'].update({
                'has_merger': True,
                'dark_merger': has_dark_merger,
                'merger_ratio': total_ratio,
                'merger_ratio_stellar_only': stellar_ratio,
                'main_progenitor': main_prog_id,
                'main_progenitor_mvir': main_prog_mvir,
                'minor_stellar_mvir': minor_stellar_mvir,
                'total_minor_mvir': total_minor_mvir,
                'progenitors': filtered_stellar_ids,
                'dark_progenitors': filtered_dark_ids,
                'rejected_minor_progenitors': rejected_stellar_ids,
                'rejected_dark_progenitors': rejected_dark_ids

            })
    elif n_prog == 1:
        # Single progenitor case
        if stellar_progenitors:
            prog_id = list(stellar_progenitors.keys())[0]
            halo_data['merger_info'].update({
                'main_progenitor': prog_id,
                'main_progenitor_mvir': stellar_progenitors[prog_id]['Mvir'],
            })
        elif dark_progenitors:
            prog_id = list(dark_progenitors.keys())[0]
            halo_data['merger_info'].update({
                'main_progenitor': prog_id,
                'main_progenitor_mvir': dark_progenitors[prog_id]['Mvir'],
            })

    else:
        print(
            f"Warning: No progenitors found for halo {halo_id} at snapshot {current_step}")

    return halo_data


def process_snapshot(main_prog, halos_later, halos_earlier, time, h,
                     current_step, num_threads=None,
                     contribution_threshold=50.0):
    """Previous documentation..."""
    if num_threads is None:
        num_threads = 1

    # get list of halos from main_prog
    halos_to_use = [halo for halo in halos_later if
                    halo.properties['halo_number'] in main_prog]

    # halos_with_stars = [halo for halo in halos if halo.properties['n_star'] > 0]

    halos_earlier_with_stars = [h for h in halos_earlier if
                                h.properties['n_star'] > 0]
    halos_earlier_dark = [h for h in halos_earlier if
                          h.properties['n_star'] == 0
                          and h.properties['npart'] > 1000]

    shared_results = pymp.shared.dict()

    with pymp.Parallel(num_threads) as p:
        for i in p.range(len(halos_to_use)):
            halo = halos_to_use[i]
            halo_id = halo.properties['halo_number']
            try:
                halo_data = process_halo(
                    halo, current_step, time, h, halo_id,
                    halos_earlier_with_stars, halos_earlier_dark,
                    contribution_threshold
                )
            except Exception as e:
                print(f"Error processing halo {halo_id}: {e}")
                traceback.print_exc()
                halo_data = None
            with p.lock:
                shared_results[halo_id] = halo_data

    merger_histories = dict(sorted(shared_results.items()))
    validate_snapshot_data(halos_to_use, merger_histories, current_step)

    print(
        f"Successfully processed and validated all {len(merger_histories)} halos in snapshot {current_step}")

    # return new main_prog for next iteration
    # main prog is the main progenitor for each halo
    main_prog = []
    for halo_id, halo_data in merger_histories.items():
        if halo_data is not None and halo_data['merger_info'][
            'main_progenitor'] is not None:
            main_prog.append(halo_data['merger_info']['main_progenitor'])
        else:
            print(f"Warning: No valid main progenitor for halo {halo_id}")

    return merger_histories, main_prog


# noinspection PyUnboundLocalVariable
def analyze_merger_history(sim_path, halos_to_use, num_snapshots=None,
                           num_threads=None):
    """
    Analyze the full merger history across available snapshots.
    """
    # Find all available snapshots
    snapshot_paths = find_simulation_snapshots(sim_path)

    if num_snapshots:
        snapshot_paths = snapshot_paths[:num_snapshots]

    print("\n=== Snapshot Analysis Plan ===")
    print(f"Found {len(snapshot_paths)} snapshots to analyze")
    for path in snapshot_paths:
        step = int(Path(path).parent.parent.name.split('.')[-1])
        print(f"  {step}: {path}")

    all_histories = {}
    main_prog = halos_to_use
    later_sim = None
    later_halos = None

    # Process snapshots in pairs
    for i in range(len(snapshot_paths) - 1):
        later_path = snapshot_paths[i]
        earlier_path = snapshot_paths[i + 1]

        later_step = int(Path(later_path).parent.parent.name.split('.')[-1])
        earlier_step = int(Path(earlier_path).parent.parent.name.split('.')[-1])

        print(f"\n{'=' * 50}")
        print(f"Processing iteration {i + 1}:")
        print(f"Current snapshot: {later_step}")
        print(f"Earlier snapshot: {earlier_step}")

        try:
            # Load later snapshot only if it's not already loaded
            if later_sim is None:
                later_sim = pynbody.load(later_path)
                later_sim.physical_units()
                later_halos = later_sim.halos(halo_numbers='v1')

            h = later_sim.properties['h']
            time = later_sim.properties['time'].in_units('Gyr')

            # Load earlier snapshot
            earlier_sim = pynbody.load(earlier_path)
            earlier_sim.physical_units()
            earlier_halos = earlier_sim.halos(halo_numbers='v1')

            # Process snapshots and get merger histories
            print(f"\nPassing to process_snapshot:")
            print(f"  - Main snapshot: {later_step}")
            print(f"  - Earlier snapshot: {earlier_step}")

            current_step = int(
                Path(later_sim.filename).parts[-3].split('.')[-1])
            print(
                f"Processing {len(main_prog)} halos with stars in snapshot {current_step}")

            history, main_prog = process_snapshot(main_prog, later_halos,
                                                  earlier_halos,
                                                  time, h, current_step,
                                                  num_threads=num_threads)

            print(f"\nStoring results in all_histories:")
            print(f"  - Key (later snapshot number): {later_step}")
            print(f"  - Number of halos processed: {len(history)}")
            all_histories[later_step] = history

            # Clean up and prepare for next iteration
            del later_sim
            del later_halos
            later_sim = earlier_sim
            later_halos = earlier_halos
            # # Clear references to earlier snapshot
            earlier_sim = None
            earlier_halos = None

        except Exception as e:
            print(f"Error processing snapshots: {e}")
            traceback.print_exc()
            # Clean up on error
            if later_sim is not None:
                del later_sim
                del later_halos
            if 'earlier_sim' in locals():
                del earlier_sim
                del earlier_halos

    print("\n=== Final Results ===")
    print("Snapshots processed and stored in all_histories:")
    for step in sorted(all_histories.keys(), reverse=True):
        print(f"  Snapshot {step}: {len(all_histories[step])} halos")

    return all_histories


def analyze_multiple_sims(base_path, pattern="*cosmo*.4096*",
                          num_snapshots=None, num_threads=None):
    """
    Analyze merger histories for multiple simulations in a directory.

    Parameters:
    base_path: path containing multiple simulation directories
    pattern: glob pattern to match simulation directories
    num_snapshots: maximum number of snapshots to analyze per simulation
    num_threads: number of threads to use for parallel processing

    Returns:
    dict: Dictionary of simulation names to their merger histories
    """
    all_sim_histories = {}

    # Find valid simulation directories
    sim_dirs = find_simulation_directories(base_path, pattern)
    print(
        f"Found {len(sim_dirs)} valid simulations matching pattern '{pattern}'")

    for sim_dir in sim_dirs:
        sim_name = sim_dir.name
        print(f"\nAnalyzing simulation: {sim_name}")

        # Find valid simulation snapshots
        snapshots = glob(f"{sim_dir}/**/ahf_200/*.??????", recursive=True)
        valid_snapshots = [snap for snap in snapshots
                           if re.search(r'\.\d{6}$', snap)
                           and not any(snap.endswith(ext) for ext in
                                       ['.parameter', '.param', '.kdtree',
                                        '.info'])]

        if not valid_snapshots:
            print(f"No valid snapshots found for {sim_name}")
            continue

        # Sort snapshots by number and get the latest
        latest_snapshot = sorted(valid_snapshots,
                                 key=lambda x: int(
                                     re.search(r'\.(\d{6})$', x).group(1)),
                                 reverse=True)[0]

        print(f"Latest snapshot: {latest_snapshot}")

        try:
            # Analyze this simulation
            histories = analyze_merger_history(
                latest_snapshot,
                num_snapshots=num_snapshots,
                num_threads=num_threads
            )
            all_sim_histories[sim_name] = histories

        except Exception as e:
            print(f"Error analyzing simulation {sim_name}: {str(e)}")
            continue

    return all_sim_histories


# # Example usage:
# if __name__ == '__main__':
#     # Analyze a single simulation
#     histories = analyze_merger_history(
#         'path/to/any/snapshot',
#         num_snapshots=5,  # Limit to 5 snapshots
#         num_threads=6
#     )
#
#     # Or analyze multiple simulations
#     all_histories = analyze_multiple_sims(
#         '/data/REPOSITORY/dwarf_volumes',
#         pattern="*cosmo*.4096*",
#         num_snapshots=5,
#         num_threads=6
#     )
import pickle

# list halos to use starting at z = 0
# read halos to use from file '../DataFiles/Marvel.z0.pickle'
Marvel_z0 = pickle.load(open('../DataFiles/Marvel.z0.pickle', 'rb'))
DCJL_z0 = pickle.load(open('../DataFiles/DCJL.z0.pickle', 'rb'))

# sim_path = '/data/REPOSITORY/dwarf_volumes/cptmarvel.cosmo25cmb.4096g5HbwK1BH/cptmarvel.cosmo25cmb.4096g5HbwK1BH.004096/ahf_200/cptmarvel.cosmo25cmb.4096g5HbwK1BH.004096'
# sims = ['cptmarvel', 'elektra', 'storm', 'rogue']
# base_path = '/data/REPOSITORY/dwarf_volumes'
# for sim in sims:
#     halos_to_use = list(Marvel_z0[sim].keys())
#     # convert to list of ints
#     halos_to_use = [int(halo) for halo in halos_to_use]
#     print(f'Analyzing {sim}')
#     sim_path = f'{base_path}/{sim}.cosmo25cmb.4096g5HbwK1BH/{sim}.cosmo25cmb.4096g5HbwK1BH.004096/ahf_200/{sim}.cosmo25cmb.4096g5HbwK1BH.004096'
#     print(sim_path)
#     # get merger history
#     history_df = analyze_merger_history(sim_path, halos_to_use, num_threads=25)
#     # save to file
#     with open(f'../DataFiles/{sim}.merger_history.pkl', 'wb') as f:
#         pickle.dump(history_df, f)
# sims = ['h148']
# base_path = '/data/REPOSITORY/e12Gals'
# for sim in sims:
#     halos_to_use = list(DCJL_z0[sim].keys())
#     # convert to list of ints
#     halos_to_use = [int(halo) for halo in halos_to_use]
#     print(f'Analyzing {sim}')
#     sim_path = f'{base_path}/{sim}.cosmo50PLK.3072g3HbwK1BH/{sim}.cosmo50PLK.3072g3HbwK1BH.004096/ahf_200/{sim}.cosmo50PLK.3072g3HbwK1BH.004096'
#     print(sim_path)
#     # get merger history
#     history_df = analyze_merger_history(sim_path, halos_to_use, num_threads=25)
#     # save to file
#     with open(f'../DataFiles/{sim}.merger_history.pkl', 'wb') as f:
#         pickle.dump(history_df, f)

sims = ['h229','h242','h329']
sims = ['h329']
base_path = '/data/REPOSITORY/e12Gals'
for sim in sims:
    halos_to_use = list(DCJL_z0[sim].keys())
    # convert to list of ints
    halos_to_use = [int(halo) for halo in halos_to_use]
    print(f'Analyzing {sim}')
    sim_path = f'{base_path}/{sim}.cosmo50PLK.3072gst5HbwK1BH/{sim}.cosmo50PLK.3072gst5HbwK1BH.004096/ahf_200/{sim}.cosmo50PLK.3072gst5HbwK1BH.004096'
    print(sim_path)
    # get merger history
    history_df = analyze_merger_history(sim_path, halos_to_use, num_threads=32)
    # save to file
    with open(f'../DataFiles/{sim}.merger_history.pkl', 'wb') as f:
        pickle.dump(history_df, f)