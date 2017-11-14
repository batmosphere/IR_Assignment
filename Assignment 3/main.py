#CODE TO EXECUTE SVD AND CUR ON MOVIE RATINGS
k = input("Enter Dimensionality for SVD (Usually the number of users): ") 
k = int(k)
r = input("enter r i.e number of rows/columns to pick in CUR : ") #enter r
r = int(r)
import svd #opening svd.py
import cur #opening cur.py
import os #import os for file exist checks
import numpy as np #numpy import
import json #import json for dumping matrices
from pympler import asizeof #import pympler for space usage estimation
import sys #importing sys for y/n confirmation

directory='./reports'
if not os.path.exists(directory):
    os.makedirs(directory)
def query_yes_no(question, default="yes"): #y/n question class
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

svd_usage=asizeof.asizeof(svd) #calculate space usage for svd
cur_usage=asizeof.asizeof(cur) #calculate space usage for cur

class MyEncoder(json.JSONEncoder): #custom class to facilitate json serialization of numpy objects
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

print('Writing report') #processing done and started output
try:
    os.remove("./reports/report.txt") #delete files if they exist in order to prevent meaningless appends
except OSError:
    pass

try:
    os.remove("./reports/matrices.json")
except OSError:
    pass

report = open("./reports/report.txt", 'a') #open report file
string = """
******************************************************************
*  ASSIGNMENT - III                                              *
*  DATASET:   ml-latest-small FROM MovieLens                     *
*  USERS: 671                                                    *
*  MOVIES: 9000                                                  *
*  RATINGS: 100004                                                *
*  MEMBER 1: Aayush Barthwal 2015A7PS0136H                       *
*  MEMBER 2: Mukund Kothari 2015A7PS0133H                        *
*  MEMBER 3: Rohitashva Vashishtha 2015B4PS0546H                 *
*  MEMBER 4: Tushar Aggarwal 2015A7PS0047H                       *
******************************************************************""" 
report.write("\n%s\n" % string) #printing ascci-art
report.write("Time taken by Collaborative Algorithm: %f" % collaborative.c_time)
report.write(" seconds\n")
report.write("Time taken by SVD Algorithm: %f" % svd.svd_time)
report.write(" seconds\n")
report.write("Time taken by CUR Algorithm: %f" % cur.cur_time)
report.write(" seconds\n")
report.write("Space taken by Collaborative Algorithm: %d" % collaborative_usage)
report.write(" KB\n")
report.write("Space taken by SVD Algorithm: %d" % svd_usage)
report.write(" KB\n")
report.write("Space taken by CUR Algorithm: %d" % cur_usage)
report.write(" KB\n")
report.write("Frobenius error in SVD: ")
print(svd.frobenius_svd,file=report)
report.write("Frobenius error in CUR: ")
print(cur.frobenius_cur,file=report)
report.write("------------------------------------------------------------------\n")
report.write("COMPARISION\n")
if svd.svd_time < cur.cur_time:
	report.write("SVD is faster\n")
else:
	report.write("CUR is faster\n")
if svd_usage < cur_usage:
	report.write("SVD is more space efficient\n")
else:
	report.write("CUR is more space efficient\n")
if svd.frobenius_svd > cur.frobenius_cur:
	report.write("CUR is more accurate\n")
else:
	report.write("SVD is more accurate\n")
report.write("------------------------------------------------------------------\n")
report.write("U matrix in SVD\n") #printing all the matrices calculated in svd and cur
print(svd.U,file=report)
report.write("------------------------------------------------------------------\n")
report.write("V Transpose matrix in SVD\n")
print(svd.V_transpose,file=report)
report.write("------------------------------------------------------------------\n")
report.write("S matrix in SVD\n")
print(svd.S,file=report)
report.write("------------------------------------------------------------------\n")
report.write("Final matrix in SVD\n")
print(svd.M2,file=report)
report.write("------------------------------------------------------------------\n")
report.write("C matrix in CUR\n")
print(cur.C,file=report)
report.write("------------------------------------------------------------------\n")
report.write("U matrix in CUR\n")
print(cur.U,file=report)
report.write("------------------------------------------------------------------\n")
report.write("R matrix in CUR\n")
print(cur.R,file=report)
report.write("------------------------------------------------------------------\n")
report.write("Final matrix in CUR\n")
print(cur.CUR,file=report)
