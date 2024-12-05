"""
Code for the publication Exploiting Flexibility in Multi-Energy Systems
through Distributionally Robust Chance-Constrained
Optimization by Marwan Mostafa 

Results File
"""
###############################################################################
## IMPORT PACKAGES & SCRIPTS ## 
###############################################################################
#### PACKAGES ####
import ast
import pandas as pd 
import pickle as pkl

#### SCRIPTS ####
import parameters as par

# Check and convert string representations of lists back to actual lists if necessary
def convert_to_list_if_needed(cell):
    if isinstance(cell, str):
        return eval(cell)
    return cell
import pandas as pd


def load_results(results_df):
    theta_degrees = results_df['theta_degrees']
    loading_percent = results_df['line_loading_percent']
    load_p_mw = results_df['load_p_mw']
    sgen_p_mw = results_df['sgen_p_mw']
    line_pl_mw = results_df['line_pl_mw']
    i_ka = results_df['line_current_mag']

    return theta_degrees, loading_percent, load_p_mw, sgen_p_mw, line_pl_mw, i_ka

def load_results_opf(results_opf_df):
    loading_percent = results_opf_df['line_loading_percent']
    ext_grid_p_mw = results_opf_df['ext_grid_p_mw']
    sgen_p_mw = results_opf_df['sgen_p_mw']
    curtailment_pv_mw = results_opf_df['curtailment_pv_mw']
    load_p_mw = results_opf_df['load_p_mw']

    return  loading_percent, ext_grid_p_mw, sgen_p_mw, curtailment_pv_mw, load_p_mw


def curtailment_calculation(results, load_profile):
    # Assuming the flexible load is at the first bus
    bus = 2
    curtailment_factor = []

    # Loop through each timestep to calculate curtailment
    for t in range(len(results['load'])):
        # Get the expected (input) load from the profile and actual load from the results
        expected_load = load_profile['P_HEATPUMP_smooth'].iloc[t] / par.hp_scaling
        actual_load = results['load'][t][bus]

        # Calculate the curtailment factor
        curtailment = (expected_load - actual_load) / expected_load if expected_load != 0 else 0
        curtailment_factor.append(curtailment)

    return curtailment_factor


def save_optim_results(results, filename):
    try:
        with open(filename, 'wb') as file:
            pkl.dump(results, file)
        print(f"Results successfully saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving the results: {e}")

def load_optim_results(filename):
    try:
        with open(filename, 'rb') as file:
            results = pkl.load(file)
        print(f"Results loaded successfully from {filename}.")
        return results
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return None
    except pkl.UnpicklingError:
        print(f"Error: Unable to load the file {filename}. It may not be a valid pickle file.")
        return None