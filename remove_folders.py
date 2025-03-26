import numpy as np 
import pandas as pd 
import os 

def main(fdirs):

    # Read the NZONE problematic runs
    problematic_runs = centers_from_file(
        base_fdir=fdirs["python_files_dir"], file_name="nzone_problematic_runs.txt"
    )

    base_fdir = fdirs["cloudy_runs_files_dir"]
    for row, center in problematic_runs.iterrows():
        fdir = f"hden{center['log_hden']:.5f}_metallicity{center['log_metallicity']:.5f}_turbulence{center['log_turbulence']:.5f}_isrf{center['log_isrf']:.5f}_radius{center['log_radius']:.5f}"
        path2folder = f"{base_fdir}/{fdir}"

        # print(path2folder)

        # Delete everything in the destination folder
        rm_cmd = f"rm -rf {path2folder}"
        delete = os.system(rm_cmd)

        # print(f"Deleted {path2folder}")

        if row % 1e2 == 0:
            print(f"{row} finished. Left {len(problematic_runs)-row} runs.")

    return None

def centers_from_file(base_fdir, file_name):
    """
    Read the problematic runs from the nzone data
    """

    data = pd.read_csv(f"{base_fdir}/{file_name}", sep=' ')

    return data

if __name__ == "__main__":
    

    fdirs = {
        "cloudy_runs_files_dir":"/scratch/m/murray/dtolgay/cloudy_runs/z_0/cr_1_CO87_CII_H_O3/cr_1_CO87_CII_H_O3_metallicity_above_minus_2",
        "python_files_dir":"/scratch/m/murray/dtolgay/cloudy_runs/z_0/cr_1_CO87_CII_H_O3/cr_1_CO87_CII_H_O3_metallicity_above_minus_2/python_files",
    }
    
    main(fdirs)