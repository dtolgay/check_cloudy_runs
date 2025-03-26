import os
import pandas as pd  # type: ignore
import numpy as np 

def determine_runs_does_not_contain_file(base_fdir, file_name="success.txt"):

    # read dirlist.txt
    file_path = "dirlist.txt"

    dirlist = []
    with open(file_path, "r") as file:
        for line in file:
            dirlist.append(line.strip())

    success_list = []
    unrunned_list = []
    for i, directory in enumerate(dirlist):
        if os.path.exists(f"{base_fdir}/{directory}/success.txt"):
            success_list.append(directory)
        else:
            unrunned_list.append(directory)

        if (i%1e3 == 0):
            print(f"Processed {i} files. Remaning {len(dirlist)-i} files.")

    # Write the successfull and unrunned runs to a file
    with open("successfull_runs.txt", "w") as file:
        for directory in success_list:
            file.write(f"{directory}\n")

    with open("unrunned_runs.txt", "w") as file:
        for directory in unrunned_list:
            file.write(f"{directory}\n")

    return None 

def determine_run_situation(base_fdir, file_identifiers_and_dirs):

    threshold_Nh = 5.6 # log(cm-3 pc)

    # read centers.txt
    file_path = f"{base_fdir}/centers.txt"
    centers = pd.DataFrame(
        np.loadtxt(file_path),
        columns=[
            "log_metallicity",
            "log_hden",
            "log_turbulence",
            "log_isrf",
            "log_radius"
        ]
    )

    # use only the centers that are below the threshold
    condition = (10**centers["log_hden"] * 10**centers["log_radius"] < 10**threshold_Nh)
    centers = centers[condition].copy() 
    # Write the centers that are below the threshold to a file
    centers.to_csv("centers_below_threshold.txt", index=False, header=True, sep=" ")
    print(f"Written centers below the threshold to centers_below_threshold.txt")


    # Identify the status of cloudy jobs 
    file_not_found = []
    keyword_not_found = []
    cloudy_folders_that_are_gonna_be_run = []

    for counter, center in centers.iterrows():

        if counter%1e3 == 0:
            print(f"Processed {counter} centers. Remaining {len(centers)-counter} centers.")
        
        fdir = f"hden{center['log_hden']:.5f}_metallicity{center['log_metallicity']:.5f}_turbulence{center['log_turbulence']:.5f}_isrf{center['log_isrf']:.5f}_radius{center['log_radius']:.5f}"
        file_path = f"{base_fdir}/{fdir}/{fdir}.out"
        
        searched_keyword_found = False  # Initialize as False
        
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
                
                # Check for "ok" first
                for line in lines:
                    if file_identifiers_and_dirs["ok"]["searched_keyword"] in line:
                        file_identifiers_and_dirs["ok"]["data"].append(center)
                        searched_keyword_found = True  # Mark as found and stop further checks
                        break
                
                # If not "ok", check for other conditions
                if not searched_keyword_found:
                    for line in lines:
                        for identifier in ["nzone", "disaster"]:
                            if file_identifiers_and_dirs[identifier]["searched_keyword"] in line:
                                file_identifiers_and_dirs[identifier]["data"].append(center)
                                searched_keyword_found = True  # Mark as found
                                break
                        if searched_keyword_found:
                            break  # Stop checking other lines once assigned
        
        except FileNotFoundError:
            file_not_found.append(center)
            searched_keyword_found = None  # Mark as missing
            if 10**center['log_hden'] * 10**center['log_radius'] < 10**threshold_Nh:
                cloudy_folders_that_are_gonna_be_run.append(fdir)  # Add to the list of folders that are gonna be run          
        
        finally:
            if searched_keyword_found is False:  # Only add if no keyword was found
                keyword_not_found.append(fdir)
                if 10**center['log_hden'] * 10**center['log_radius'] < 10**threshold_Nh:
                    cloudy_folders_that_are_gonna_be_run.append(fdir)


    # Check if there are any duplicate centers in "ok" and "nzone"
    ok_centers = set(tuple(row) for row in file_identifiers_and_dirs["ok"]["data"])
    nzone_centers = set(tuple(row) for row in file_identifiers_and_dirs["nzone"]["data"])

    # Find intersections
    duplicate_centers = ok_centers.intersection(nzone_centers)

    for center in duplicate_centers:
        print(f"Center {center} is in both ok and nzone.")

    # Write the data to the files
    for identifier, file_identifier_and_dir in file_identifiers_and_dirs.items():
        data = file_identifier_and_dir["data"]
        data = pd.DataFrame(data, columns=[
            "log_metallicity",
            "log_hden",
            "log_turbulence",
            "log_isrf",
            "log_radius"
        ])
        data.to_csv(file_identifier_and_dir["file_name"], index=False, header=True, sep=" ")
        print(f"Written {identifier} data to {file_identifier_and_dir['file_name']}")

    # Write the file not found data to a file
    data = pd.DataFrame(file_not_found, columns=[
        "log_metallicity",
        "log_hden",
        "log_turbulence",
        "log_isrf",
        "log_radius"
    ])
    data.to_csv("file_not_found.txt", index=False, header=True, sep=" ")
    print(f"Written file not found data to file_not_found.txt")

    # Write the keyword_not_found data to a file
    data = pd.DataFrame(keyword_not_found, columns=[
        # "log_metallicity",
        # "log_hden",
        # "log_turbulence",
        # "log_isrf",
        # "log_radius"
        "file_name"
    ])
    data.to_csv("keyword_not_found.txt", index=False, header=True, sep=" ")
    print(f"Written keyword_not_found jobs to keyword_not_found.txt")


    # Write the cloudy_folders_that_are_gonna_be_run data to a file
    data = pd.DataFrame(cloudy_folders_that_are_gonna_be_run, columns=[
        "file_name"
    ])
    data.to_csv("cloudy_folders_that_are_gonna_be_run.txt", index=False, header=True, sep=" ")
    print(f"Written cloudy_folders_that_are_gonna_be_run jobs to cloudy_folders_that_are_gonna_be_run.txt")

    return None



if __name__ == '__main__':

    file_identifiers_and_dirs = {
        "ok": {
            "searched_keyword": " [Stop in cdMain at maincl.cpp:593, Cloudy exited OK]",
            "file_name": "ok_runs.txt",
            "data": [] 
            },
        "nzone": {
            "searched_keyword": " W-Calculation stopped because default number of zones reached.  Was this intended???",
            "file_name": "nzone_problematic_runs.txt",
            "data": []
            },
        "disaster": {
            "searched_keyword": "DISASTER",
            "file_name": "disaster_runs.txt",
            "data": []
            },
        }

    base_fdir = "/scratch/m/murray/dtolgay/cloudy_runs/z_0/cr_1_CO87_CII_H_O3/cr_1_CO87_CII_H_O3_metallicity_above_minus_2"

    determine_run_situation(base_fdir, file_identifiers_and_dirs)
    # determine_runs_does_not_contain_file(base_fdir, file_name="success.txt")