import os as os
import shutil as shutil
import yaml as yaml
import sys

PATH = str(sys.argv[1])

#Provide either flag for checking redundancy or for copying folders
FLAG = str(sys.argv[2])

print(PATH)

#Insert teams according to KU-ID
#Example:
team1 = ["vwf342", "gqh329", "nrd664"] 
team2 = ["mzd685", "cxm492", "czw500"] 
team3 = ["jld357", "dwr593", "rzm597"] 
team4 = ["qjx187", "czw487", "xwv793"]
#team5 = ["qxj826", "cjq296", "dxl229"] 
team6 = ["bwg212", "cjx555", "ctq409"] 
#team7 = ["lnc290", "wkd914"]


teams = [team1, team2, team3, team4, team6]

# create a lists of directory names in folder
def get_names(folder_path):
    names = []
    for name in os.listdir(folder_path):
        #Exclude hidden files
        if not name.startswith('.'):
            names.append(name)
    return names

# check that exactly one name from a folder is in each list
# Otherwise the ku-ids of conflicting handins will be printed and False returned
def check_names(folder_path):
    result = True
    names = get_names(folder_path)
    for team in teams:
        count = 0
        for name in names:
            if name in team:
                count += 1
        if count != 1:
            result = False
            print(f"Error: Wrong number handins from team: {team}")
    if result:
        print("No redunant handins were detected")
    return result

def match_student_data(folder_path):
    if not(check_names(PATH)):
        print("Please cleanup redundant handins before perfoming this action")
        exit(1)
    names = get_names(folder_path)
    for name in names:
        if name != "empty.yml" and name != "meta.yml":
            #find the other names in the team
            team_mates = []
            for team in teams:
                if name in team:
                    team_mates = team
                    break
            #copy the folder of name and create a new folder for each team mate
            team_mate_data = []
            for team_mate in team_mates:
                if team_mate != name:
                    team_mate_data.append(find_student_data(team_mate))
            contents = None
            with open((PATH+"/"+name+"/grade.yml"), "r") as read_file:
                contents = yaml.safe_load(read_file)
                for mate in team_mate_data:
                    contents['students'].append(mate)
            with open(PATH+"/"+name+"/grade.yml", "w") as write_file:
                yaml.dump(contents, write_file)


def find_student_data(ku_id):
    left_students = []
    with open (PATH+"/empty.yml", "r") as read_file:
        contents = yaml.safe_load(read_file)
        left_students = list(contents)
    for student in left_students:
        if list(student.values())[0]['login'][:6] == ku_id:
            return student
    return None

#Main Entrypoint
def main():
    if FLAG == "--check":
        print("Checking")
        check_names(PATH)
    elif FLAG == "--copy":
        match_student_data(PATH)
        #change_student_data(PATH)
        print("Finished. Ready to upload to canvas using staffeli_nt")
    else:
        print("Usage: gradingfile.py PATH [-check | -copy]")
        exit(1)

if __name__ == "__main__":
    main()