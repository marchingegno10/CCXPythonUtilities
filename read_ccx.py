"""
Created on Sat Mar  18 09:52:46 2023

@author: marchingegno10

this function reads the .dat file of a ccx *STATIC step calculation storing every variable in a dictionary of dictionaries. For example, if you decided to print the displacements (U) and the plastic strain (PEEQ), a dictionary of two dictionaries will be created. In this case the .dat file will be something like this:

 displacements (vx,vy,vz) for set NALL and time  0.1000000E+01

     1  0.000000E+00  0.000000E+00  0.000000E+00
     2 -1.960390E-07 -1.334919E-07  7.866892E-07
     3 -7.734289E-07  1.485305E-07  1.595261E-06
     4 -1.392737E-06  2.675306E-07  2.212376E-06
     5 -1.988940E-06  1.665039E-07  2.948853E-06
     6 -2.641016E-06 -1.534262E-07  3.961862E-06
     7 -3.471381E-06 -6.531946E-07  5.120239E-06
     8 -5.691419E-06 -2.568090E-06  8.595325E-06
     9 -5.507970E-06 -1.062992E-05  1.772012E-05
     10 -9.493931E-07 -1.796107E-05  2.344208E-05
     ..  ............  ............  ............

 equivalent plastic strain (elem, integ.pnt.,pe)for set C3D10 and time  0.1000000E+01

     12303   1  3.182005E-05
     12303   2  4.403311E-05
     12303   3  4.130446E-05
     12303   4  7.451935E-06
     12304   1  0.000000E+00
     12304   2  0.000000E+00
     12304   3  0.000000E+00
     12304   4  0.000000E+00
     12305   1  5.265799E-04
     12305   2  2.247397E-04
     12305   3  4.789547E-04
     12305   4  3.520450E-04
     12306   1  1.659073E-04
     ...     .  ............

So, this function will return a dictionary (let's say 'data') containing the two dictionaries data['displacements'] and data['equivalent plastic strain']. Each of them, has a certain number of lists depending on the variable. For example, we can have access to displacement in y direction typing data['displacements']['vy']; if I want to get the equivalent plastic strain, I type data['equivalent plastic strain']['pe'].

"""

def read_ccx(filename): #the name of the file you want to read
    fhand = open(filename, 'r')
    lines = fhand.readlines()
    fhand.close()
    stuff = list()
    data = dict()

    for line in lines:
        stuff.append(line.split())
    stuff.append([]) #in order to st[<32;37;35Mop the reading at the end of the file

    for i in range(0,len(lines)):
        if not '(' in lines[i]:
            continue
        else:
            if 'elem' in lines[i]:
                pos_0 = lines[i].find('(')
                pos_f = lines[i].find(')')
                head = lines[i][pos_0+1:pos_f].split(',')
                for t in range(len(head)): #remove spaces
                    head[t] = head[t].strip()
                var = lines[i].split('(')[0].strip()
                data[var] = dict()
                for j in range(len(head)):
                    data[var][head[j]] = list()
                    k = 0
                    while stuff[i+2+k] != []:
                        data[var][head[j]].append(float(stuff[i+2+k][j]))
                        k += 1
            elif 'elem' not in lines[i]: #in order to read *NODE PRINT
                pos_0 = lines[i].find('(')
                pos_f = lines[i].find(')')
                head = lines[i][pos_0+1:pos_f].split(',')
                head.insert(0, 'node')
                for t in range(len(head)): #remove spaces
                    head[t] = head[t].strip()
                var = lines[i].split('(')[0].strip()
                data[var] = dict()
                for j in range(len(head)):
                    data[var][head[j]] = list()
                    k = 0
                    while stuff[i+2+k] != []:
                        data[var][head[j]].append(float(stuff[i+2+k][j]))
                        k += 1
    return data

