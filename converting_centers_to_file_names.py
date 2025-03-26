import pandas as pd 

def main(path2dir, file_name):

    centers = centers_from_file(path2dir, file_name)

    file_names = []
    for row, center in centers.iterrows():
        file_name = f"hden{center['log_hden']:.5f}_metallicity{center['log_metallicity']:.5f}_turbulence{center['log_turbulence']:.5f}_isrf{center['log_isrf']:.5f}_radius{center['log_radius']:.5f}"
        
        file_names.append(file_name)



    # Write the file_names to a file
    fdir = f"{path2dir}/cloudy_folders_that_are_gonna_be_run_nzone_problematic.txt"
    with open(fdir, "w") as f:
        for file_name in file_names:
            f.write(f"{file_name}\n")

    print(f"File is written to {fdir}")

    return None


def centers_from_file(base_fdir, file_name):
    """
    Read the problematic runs from the nzone data
    """

    data = pd.read_csv(f"{base_fdir}/{file_name}", sep=' ')

    return data


if __name__ == '__main__':

    path2dir = "/scratch/m/murray/dtolgay/cloudy_runs/z_0/cr_1_CO87_CII_H_O3/cr_1_CO87_CII_H_O3_metallicity_above_minus_2/python_files"
    file_name = "nzone_problematic_runs.txt"

    main(path2dir, file_name)