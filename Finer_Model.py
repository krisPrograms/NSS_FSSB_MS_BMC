# Import the SAT solvers and a timekeeping module
from pysat.solvers import Glucose3
from pysat.solvers import Gluecard3
from pysat.solvers import Lingeling
import time

# Create the SAT solvers
solver1 = Glucose3()
solver2 = Gluecard3()
solver3 = Lingeling()

# Set the number of intervals for chemicals
numIntervals = 5

# Set the scale factor for the finer model
scaleFactor = 4

# Get k value for BMC from the user
k = int(input("Enter k value: "))
print("K value:", k)

# Set the properties to check
numProperties = 1
negatedProperties = []
negatedProperty = "-6"
negatedProperty = negatedProperty.split()
negatedProperties.append(negatedProperty)

# List of chemicals to reference
chemicals = ["raf", "rkip", "raf1rkip", "erkpp", "raf1rkiperkpp", "erkp",
             "rkipp", "rp", "mek", "mekpp", "mekpperk", "rkipprp", "mekraf"]

num_chemicals = len(chemicals)

# Lists for the min and max of each chemical
srange = [200, 2,  40, 100, 200, 10, 200, 600, 200, 100, 200, 100, 100]
erange = [700, 16, 140, 1800, 500, 50, 220, 1800, 800, 720, 500, 500, 500]

# Compute the intervals
ranges = []
for i in range(len(chemicals)):
    ranges.append(erange[i] - srange[i])

# Compute the size of each interval (varies by chemical)
rangeSizes = []
for i in range(len(chemicals)):
    rangeSizes.append(ranges[i] // numIntervals)

# Creates a list of lists with all the intervals for the chemicals
num_intervals = 0
intervals = list()
intervalSymbols = list() # list of the numbers/symbols used in the machine-readable SAT formula (each corresponds with a chemical and interval)
currentSymbol = 0
for i in range(len(chemicals)):
    currentSymbol += 1
    intervals.append([]) # add a new chemical to the intervals list (empty list to store its intervals)
    intervalSymbols.append([])
    intervals[i].append(0) # add the ZERO interval
    intervalSymbols[i].append(currentSymbol)
    num_intervals += 1
    currentVal = 0
    nextVal = srange[i]
    for j in range(numIntervals - 1): # for each new interval, add it to the chemical in the intervals list and create a symbol for it
        currentSymbol += 1
        intervals[i].append((currentVal, nextVal))
        intervalSymbols[i].append(currentSymbol)
        num_intervals += 1
        currentVal = nextVal
        nextVal += rangeSizes[i]
    intervals[i].append((currentVal, erange[i]))
    num_intervals += 1
    currentSymbol += 1
    intervalSymbols[i].append(currentSymbol)

# Set initial reaction and chemical intervals
reaction = 1
raf = numIntervals - 1 # highest interval
rkip = numIntervals - 1 # highest interval
raf1rkip = 0 # ZERO interval
erkpp = numIntervals - 1 # highest interval
raf1rkiperkpp = 0 # ZERO interval
erkp = 0 # ZERO interval
rkipp = 0 # ZERO interval
rp = numIntervals - 1 # highest interval
mek = 0 # ZERO interval
mekpp = numIntervals - 1 # highest interval
mekpperk = 0 # ZERO interval
rkipprp = 0 # ZERO interval
mekraf = 0 # ZERO interval

# Function to quickly calculate chemical midpoints
def findMid(chemicalIndex, chemical):
    # If the interval is simply zero, return this
    chem_int = intervals[chemicalIndex][chemical]
    if chem_int == 0:
        return 0
    else:
        # Otherwise, get the min and max of the interval and average them
        chem_start = chem_int[0]
        chem_end = chem_int[1]
        chem_mid = (chem_start + chem_end) // 2
        return chem_mid

# Function to check which interval a value falls in
def getInterval(chemicalIndex, value):
    # If the interval is ZERO, return 0 (first interval)
    if value == 0:
        return 0
    else:
        # If not zero, look through the intervals to find the match. Return the index for it
        for i in range(1, numIntervals):
            interval_start = intervals[chemicalIndex][i][0]
            interval_end = intervals[chemicalIndex][i][1]
            if interval_start <= value <= interval_end:
                return i
        return numIntervals

# Lists to store human-readable SAT formulas for debugging
cnf1 = list()

# Function to add a clause to the correct SAT formula
def create_clause(chemicalIndex, chemicalOld):
    # Create an empty list for the clause and add the correct symbol to it, along with the negations of all other symbols for that chemical
    clause = []
    clause.append(intervalSymbols[chemicalIndex][chemicalOld])
    for i in range(len(intervals[chemicalIndex])):
        if i != chemicalOld:
            clause.append(-1 * intervalSymbols[chemicalIndex][i])
    # Add the newly generated clause to each SAT solver and the text preview
    solver1.add_clause(clause)
    solver2.add_clause(clause)
    solver3.add_clause(clause)
    cnf1.append(clause)

# Print interval key and add to list
intervalKey = [0]
print("Interval Key:")
chemindexloop = 0
for chemical in chemicals:
    print(chemical + ":")
    interval_no = 0
    for interval in intervals[chemindexloop]:
        if interval_no == 0:
            print("ZERO: " + str(intervalSymbols[chemindexloop][interval_no]))
            intervalKey.append(chemical + " = ZERO")
        else:
            print("S" + str(interval[0]) + "E" + str(interval[1]) + ": " + str(intervalSymbols[chemindexloop][interval_no]))
            intervalKey.append(chemical + " = S" + str(interval[0]) + "E" + str(interval[1]))
        interval_no += 1
    chemindexloop += 1
    print()

# Converts properties to integers to be used when adding to formula
for propertyNo in negatedProperties:
    for i in range(len(propertyNo)):
        propertyNo[i] = int(propertyNo[i])

# Reaction 1 (raf1 + rkip -> raf1rkip)

# Compute midpoints for each chemical using the function above
rafMid = findMid(0, raf)
rkipMid = findMid(1, rkip)
raf1rkipMid = findMid(2, raf1rkip)

# Ensure the reaction inputs are nonzero before proceeding
if rafMid > 0 and rkipMid > 0:
    if k > 0:
        # Add the initial chemical intervals
        create_clause(0, raf)
        create_clause(1, rkip)
        create_clause(2, raf1rkip)
        k -= 1

    # Find the minimum of the two inputs
    minMid = min(rafMid, rkipMid)

    # Calculate the product of the reaction (minMid * rate of reaction)
    product = (minMid * 0.5228) / scaleFactor

    # Move concentration from the input to output chemicals scaleFactor times and add to SAT formula to increase states
    for i in range(scaleFactor):
        # Subtract this value from each of the input chemicals
        rafMid -= product
        rkipMid -= product

        # Add the product to the output chemical (2 inputs, so the product will be multiplied by 2)
        raf1rkipMid += (product * 2)

        # Set the new chemical concentration intervals by finding the intervals that correspond to the midpoints
        raf = getInterval(0, rafMid)
        rkip = getInterval(1, rkipMid)
        raf1rkip = getInterval(2, raf1rkipMid)

        # If the BMC bound has not yet been hit, add new clauses to the SAT formula
        if k > 0:
            # Add the new chemical intervals
            create_clause(0, raf)
            create_clause(1, rkip)
            create_clause(2, raf1rkip)
            k -= 1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Reaction 2 (raf1rkip + erkpp -> raf1rkiperkpp)
# Compute midpoints for each chemical using the function above
reaction = 2
raf1rkipMid = findMid(2, raf1rkip)
erkppMid = findMid(3, erkpp)
raf1rkiperkppMid = findMid(4, raf1rkiperkpp)

# Ensure the reaction inputs are nonzero before proceeding
if raf1rkipMid > 0 and erkppMid > 0:
    # Add the initial chemical intervals
    if k > 0:
        create_clause(2, raf1rkip)
        create_clause(3, erkpp)
        create_clause(4, raf1rkiperkpp)
        k -= 1

    # Find the minimum of the two inputs
    minMid = min(raf1rkipMid, erkppMid)

    # Calculate the product of the reaction (minMid * rate of reaction)
    product = minMid * 0.62255 / scaleFactor

    # Move concentration from the input to output chemicals scaleFactor times and add to SAT formula to increase states
    for i in range(scaleFactor):
        # Subtract this value from each of the input chemicals
        raf1rkipMid -= product
        erkppMid -= product

        # Add the product to the output chemical (2 inputs, so the product will be multiplied by 2)
        raf1rkiperkppMid += (product * 2)

        raf1rkip = getInterval(2, raf1rkipMid)
        erkpp = getInterval(3, erkpp)
        raf1rkiperkpp = getInterval(4, raf1rkiperkpp)

        # If the BMC bound has not yet been hit, add new clauses to the SAT formula
        if k > 0:
            # Add the new chemical intervals
            create_clause(2, raf1rkip)
            create_clause(3, erkpp)
            create_clause(4, raf1rkiperkpp)
            k -= 1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Reaction 3 (raf1rkiperkpp -> raf1 + erkp + rkipp)
# Compute midpoints for each chemical using the function above
reaction = 3
raf1rkiperkppMid = findMid(4, raf1rkiperkpp)
rafMid = findMid(0, raf)
erkpMid = findMid(5, erkp)
rkippMid = findMid(6, rkipp)

# Ensure the reaction input is nonzero before proceeding
if raf1rkiperkppMid > 0:
    # Add the initial chemical intervals
    if k > 0:
        create_clause(4, raf1rkiperkpp)
        create_clause(0, raf)
        create_clause(5, erkp)
        create_clause(6, rkipp)
        k -= 1

    # Calculate the product of the reaction (minMid * rate of reaction)
    product = raf1rkiperkppMid * 0.0315 / scaleFactor

    # Move concentration from the input to output chemicals scaleFactor times and add to SAT formula to increase states
    for i in range(scaleFactor):
        # Subtract this value from the input chemical
        raf1rkiperkppMid -= product

        # Add the product to the output chemicals (3 outputs, so the product will be divided by 3)
        rafMid += (product / 3)
        erkpMid += (product / 3)
        rkippMid += (product / 3)

        raf1rkiperkpp = getInterval(4, raf1rkiperkpp)
        raf = getInterval(0, rafMid)
        erkp =  getInterval(5, erkpMid)
        rkipp =  getInterval(6, rkippMid)

        # If the BMC bound has not yet been hit, add new clauses to the SAT formula
        if k > 0:
            # Add the new chemical intervals
            create_clause(4, raf1rkiperkpp)
            create_clause(0, raf)
            create_clause(5, erkp)
            create_clause(6, rkipp)
            k -= 1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Reaction 4 (rkipp + rp -> rkipprp)(first loop)
# Compute midpoints for each chemical using the function above
reaction = 4
rkippMid = findMid(6, rkipp)
rpMid = findMid(7, rp)
rkipprpMid = findMid(11, rkipprp)

# Ensure the reaction inputs are nonzero before proceeding
if rkippMid > 0 and rpMid > 0:
    # Add the initial chemical intervals
    if k > 0:
        create_clause(6, rkipp)
        create_clause(7, rp)
        create_clause(11, rkipprp)
        k -= 1

    # Find the minimum of the two inputs
    minMid = min(rkippMid, rpMid)

    # Calculate the product of the reaction (minMid * rate of reaction)
    product = minMid * 0.91878 / scaleFactor

    # Move concentration from the input to output chemicals scaleFactor times and add to SAT formula to increase states
    for i in range(scaleFactor):
        # Subtract this value from each of the input chemicals
        rkippMid -= product
        rpMid -= product

        # Add the product to the output chemical (2 inputs, so the product will be multiplied by 2)
        rkipprpMid += (product * 2)

        rkipp = getInterval(6, rkippMid)
        rp = getInterval(7, rpMid)
        rkipprp = getInterval(11, rkipprpMid)

        # If the BMC bound has not yet been hit, add new clauses to the SAT formula
        if k > 0:
            # Add the new chemical intervals
            create_clause(6, rkipp)
            create_clause(7, rp)
            create_clause(11, rkipprp)
            k -= 1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Reaction 5 (rkipprp -> rkip + rp)
# Compute midpoints for each chemical using the function above
reaction = 5
rkipprpMid = findMid(11, rkipprp)
rkipMid = findMid(1, rkip)
rpMid = findMid(7, rp)

# Ensure the reaction input is nonzero before proceeding
if rkipprpMid > 0:
    # Add the initial chemical intervals
    if k > 0:
        create_clause(11, rkipprp)
        create_clause(1, rkip)
        create_clause(7, rp)
        k -= 1

    # Calculate the product of the reaction (minMid * rate of reaction)
    product = rkipprpMid * 0.0315 / scaleFactor

    # Move concentration from the input to output chemicals scaleFactor times and add to SAT formula to increase states
    for i in range(scaleFactor):
        # Subtract this value from the input chemical
        rkipprpMid -= product

        # Add the product to the output chemicals (2 outputs, so the product will be divided by 2)
        rkipMid += (product / 2)
        rpMid += (product / 2)

        rkipprp = getInterval(11, rkipprpMid)
        rkip = getInterval(1, rkipMid)
        rp =  getInterval(7, rpMid)

        # If the BMC bound has not yet been hit, add new clauses to the SAT formula
        if k > 0:
            # Add the new chemical intervals
            create_clause(11, rkipprp)
            create_clause(1, rkip)
            create_clause(7, rp)
            k -= 1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Reaction 6 (mekpp + erkp -> mekpperkp)(second loop)
# Compute midpoints for each chemical using the function above
reaction = 6
mekppMid = findMid(9, mekpp)
erkpMid = findMid(5, erkp)
mekpperkpMid = findMid(10, mekpperk)

# Ensure the reaction inputs are nonzero before proceeding
if mekppMid > 0 and erkpMid > 0:
    # Add the initial chemical intervals
    if k > 0:
        create_clause(9, mekpp)
        create_clause(5, erkp)
        create_clause(10, mekpperk)
        k -= 1

    # Find the minimum of the two inputs
    minMid = min(mekppMid, erkpMid)

    # Calculate the product of the reaction (minMid * rate of reaction)
    product = minMid * 0.7925 / scaleFactor

    # Move concentration from the input to output chemicals scaleFactor times and add to SAT formula to increase states
    for i in range(scaleFactor):
        # Subtract this value from each of the input chemicals
        mekppMid -= product
        erkpMid -= product

        # Add the product to the output chemical (2 inputs, so the product will be multiplied by 2)
        mekpperkpMid += (product * 2)

        mekpp = getInterval(9, mekppMid)
        erkp = getInterval(5, erkpMid)
        mekpperk = getInterval(10, mekpperkpMid)

        # If the BMC bound has not yet been hit, add new clauses to the SAT formula
        if k > 0:
            # Add the new chemical intervals
            create_clause(9, mekpp)
            create_clause(5, erkp)
            create_clause(10, mekpperk)
            k -= 1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Reaction 7 (mekpperkp -> erkpp + mekpp)
# Compute midpoints for each chemical using the function above
reaction = 7
mekpperkpMid = findMid(10, mekpperk)
erkppMid = findMid(3, erkpp)
mekppMid = findMid(9, mekpp)

# Ensure the reaction input is nonzero before proceeding
if mekpperkpMid > 0:
    # Add the initial chemical intervals
    if k > 0:
        create_clause(10, mekpperk)
        create_clause(3, erkpp)
        create_clause(9, mekpp)
        k -= 1

    # Calculate the product of the reaction (minMid * rate of reaction)
    product = mekpperkpMid * 0.071 / scaleFactor

    # Move concentration from the input to output chemicals scaleFactor times and add to SAT formula to increase states
    for i in range(scaleFactor):
        # Subtract this value from the input chemical
        mekpperkpMid -= product

        # Add the product to the output chemicals (2 outputs, so the product will be divided by 2)
        erkppMid += (product / 2)
        mekppMid += (product / 2)

        mekpperk = getInterval(10, mekpperkpMid)
        erkpp = getInterval(3, erkppMid)
        mekpp =  getInterval(9,mekppMid)

        # If the BMC bound has not yet been hit, add new clauses to the SAT formula
        if k > 0:
            # Add the new chemical intervals
            create_clause(10, mekpperk)
            create_clause(3, erkpp)
            create_clause(9, mekpp)
            k -= 1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Reaction 8 (mekpp -> mek)
# Compute midpoints for each chemical using the function above
reaction = 8
mekppMid = findMid(9, mekpp)
mekMid = findMid(8, mek)

# Ensure the reaction input is nonzero before proceeding
if mekppMid > 0:
    # Add the initial chemical intervals
    if k > 0:
        create_clause(9, mekpp)
        create_clause(8, mek)
        k -= 1

    # Calculate the product of the reaction (minMid * rate of reaction)
    product = mekppMid * 0.02 / scaleFactor

    # Move concentration from the input to output chemicals scaleFactor times and add to SAT formula to increase states
    for i in range(scaleFactor):
        # Subtract this value from the input chemical
        mekppMid -= product

        # Add the product to the output chemical
        mekMid += product

        mekpp = getInterval(9, mekppMid)
        mek = getInterval(8, mekMid)

        # If the BMC bound has not yet been hit, add new clauses to the SAT formula
        if k > 0:
            # Add the new chemical intervals
            create_clause(9, mekpp)
            create_clause(8, mek)
            k -= 1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Reaction 9 (mek + raf1 -> mekraf1)
# Compute midpoints for each chemical using the function above
reaction = 9
mekMid = findMid(8, mek)
rafMid = findMid(0, raf)
mekraf1Mid = findMid(12, mekraf)

# Ensure the reaction inputs are nonzero before proceeding
if mekMid > 0 and rafMid > 0:
    # Add the initial chemical intervals
    if k > 0:
        create_clause(8, mek)
        create_clause(0, raf)
        create_clause(12, mekraf)
        k -= 1

    # Find the minimum of the two inputs
    minMid = min(mekMid, rafMid)

    # Calculate the product of the reaction (minMid * rate of reaction)
    product = minMid * 0.02 / scaleFactor

    # Move concentration from the input to output chemicals scaleFactor times and add to SAT formula to increase states
    for i in range(scaleFactor):
        # Subtract this value from each of the input chemicals
        mekMid -= product
        rafMid -= product

        # Add the product to the output chemical (2 inputs, so the product will be multiplied by 2)
        mekraf1Mid += (product * 2)

        mek = getInterval(8, mekMid)
        raf = getInterval(0, rafMid)
        mekraf = getInterval(12, mekraf1Mid)

        # If the BMC bound has not yet been hit, add new clauses to the SAT formula
        if k > 0:
            # Add the new chemical intervals
            create_clause(8, mek)
            create_clause(0, raf)
            create_clause(12, mekraf)
            k -= 1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Reaction 10 (mekraf1 -> raf1 + mekpp)
# Compute midpoints for each chemical using the function above
reaction = 10
mekraf1Mid = findMid(12, mekraf)
rafMid = findMid(0, raf)
mekppMid = findMid(9, mekpp)

# Ensure the reaction input is nonzero before proceeding
if mekraf1Mid > 0:
    # Add the initial chemical intervals
    if k > 0:
        create_clause(12, mekraf)
        create_clause(0, raf)
        create_clause(9, mekpp)
        k -= 1

    # Calculate the product of the reaction (minMid * rate of reaction)
    product = mekraf1Mid * 0.06 / scaleFactor

    # Move concentration from the input to output chemicals scaleFactor times and add to SAT formula to increase states
    for i in range(scaleFactor):
        # Subtract this value from the input chemical
        mekraf1Mid -= product

        # Add the product to the output chemicals (2 outputs, so the product will be divided by 2)
        rafMid += (product / 2)
        mekppMid += (product / 2)

        mekraf = getInterval(12, mekraf1Mid)
        raf = getInterval(0, rafMid)
        mekpp =  getInterval(9,mekppMid)

        # If the BMC bound has not yet been hit, add new clauses to the SAT formula
        if k > 0:
            # Add the new chemical intervals
            create_clause(12, mekraf)
            create_clause(0, raf)
            create_clause(9, mekpp)
            k -= 1

# Add the property to check to both SAT formulas (both computer- and human-readable)
for propertyVal in negatedProperties:
    solver1.add_clause(propertyVal)
    solver2.add_clause(propertyVal)
    solver3.add_clause(propertyVal)
    cnf1.append(propertyVal)

# Print the human-readable SAT formula
print("CNF 1:")
print(cnf1)
outString = ""
for clause in cnf1:
    for value in clause:
        if value > 0:
            outString += intervalKey[value] + " OR "
        else:
            outString += "-(" + intervalKey[-1 * value] + ")" + " OR "
    outString = outString[:-4]
    outString +=  " AND\n\n"
outString = outString[:-5]
print(outString)

# Solve the formulas and output elapsed time with Glucose3
print("Solving Formula using Glucose3...")
startTime = time.time()
print(solver1.solve())
endTime = time.time()
elapsedTime = endTime - startTime
print("Elapsed Time for Formula with Glucose3: " + str(elapsedTime))

# Solve the formulas and output elapsed time with Gluecard3
print("\nSolving Formula using Gluecard3...")
startTime = time.time()
print(solver2.solve())
endTime = time.time()
elapsedTime = endTime - startTime
print("Elapsed Time for Formula with Gluecard3: " + str(elapsedTime))

# Solve the formulas and output elapsed time with Lingeling
print("\nSolving Formula using Lingeling...")
startTime = time.time()
print(solver3.solve())
endTime = time.time()
elapsedTime = endTime - startTime
print("Elapsed Time for Formula with Lingeling: " + str(elapsedTime))