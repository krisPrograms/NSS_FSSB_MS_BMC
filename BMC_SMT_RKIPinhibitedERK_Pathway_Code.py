from z3 import *

# Create the Z3 solver
solver = Solver()

# Variable definitions
# Reaction 1 variables
raf1R1Initial = Real('raf1R1Initial')
rkipR1Initial = Real('rkipR1Initial')
raf1rkipR1Initial = Real('raf1rkipR1Initial')

raf1R1Final = Real('raf1R1Final')
rkipR1Final = Real('rkipR1Final')
raf1rkipR1Final = Real('raf1rkipR1Final')

# Reaction 2 variables
raf1rkipR2Initial = Real('raf1rkipR2Initial')
erkppR2Initial = Real('erkppR2Initial')
raf1rkiperkppR2Initial = Real('raf1rkiperkppR2Initial')

raf1rkipR2Final = Real('raf1rkipR2Final')
erkppR2Final = Real('erkppR2Final')
raf1rkiperkppR2Final = Real('raf1rkiperkppR2Final')

# Reaction 3 variables
# Create Real values for each chemical to use with the Z3 solver
raf1rkiperkppR3Initial = Real('raf1rkiperkppR3Initial')
raf1R3Initial = Real('raf1R3Initial')
erkpR3Initial = Real('erkpR3Initial')
rkippR3Initial = Real('rkippR3Initial')

raf1rkiperkppR3Final = Real('raf1rkiperkppR3Final')
raf1R3Final = Real('raf1R3Final')
erkpR3Final = Real('erkpR3Final')
rkippR3Final = Real('rkippR3Final')

# Reaction 4 variables
rkippR4Initial = Real('rkippR4Initial')
rpR4Initial = Real('rpR4Initial')
rkipprpR4Initial = Real('rkipprpR4Initial')

rkippR4Final = Real('rkippR4Final')
rpR4Final = Real('rpR4Final')
rkipprpR4Final = Real('rkipprpR4Final')

def build_model(SMTsolver, k_bound):
    if k_bound >= 1:
        # Reaction 1: raf1 + rkip = raf1rkip
        # Rate of Reaction: 0.5228
        # Ranges: 200-700, 2-16, 40-140

        # Add constraints to represent each chemical interval
        # raf1: ZERO, S0E200, S200E300, S300E400, S400E500, S500E700
        raf1R1InitialInterval1 = (raf1R1Initial == 0)
        raf1R1InitialInterval2 = And(raf1R1Initial > 0, raf1R1Initial <= 200)
        raf1R1InitialInterval3 = And(raf1R1Initial > 200, raf1R1Initial <= 300)
        raf1R1InitialInterval4 = And(raf1R1Initial > 300, raf1R1Initial <= 400)
        raf1R1InitialInterval5 = And(raf1R1Initial > 400, raf1R1Initial <= 500)
        raf1R1InitialInterval6 = And(raf1R1Initial > 500, raf1R1Initial <= 700)
        raf1R1InitialConstraints = Or(raf1R1InitialInterval1, raf1R1InitialInterval2, raf1R1InitialInterval3,
                                      raf1R1InitialInterval4, raf1R1InitialInterval5, raf1R1InitialInterval6)

        raf1R1FinalInterval1 = (raf1R1Final == 0)
        raf1R1FinalInterval2 = And(raf1R1Final > 0, raf1R1Final <= 200)
        raf1R1FinalInterval3 = And(raf1R1Final > 200, raf1R1Final <= 300)
        raf1R1FinalInterval4 = And(raf1R1Final > 300, raf1R1Final <= 400)
        raf1R1FinalInterval5 = And(raf1R1Final > 400, raf1R1Final <= 500)
        raf1R1FinalInterval6 = And(raf1R1Final > 500, raf1R1Final <= 700)
        raf1R1FinalConstraints = Or(raf1R1FinalInterval1, raf1R1FinalInterval2, raf1R1FinalInterval3,
                                    raf1R1FinalInterval4, raf1R1FinalInterval5, raf1R1FinalInterval6)

        # rkip: ZERO, S0E2, S2E4, S4E6, S6E8, S8E16
        rkipR1InitialInterval1 = (rkipR1Initial == 0)
        rkipR1InitialInterval2 = And(rkipR1Initial > 0, rkipR1Initial <= 2)
        rkipR1InitialInterval3 = And(rkipR1Initial > 2, rkipR1Initial <= 4)
        rkipR1InitialInterval4 = And(rkipR1Initial > 4, rkipR1Initial <= 6)
        rkipR1InitialInterval5 = And(rkipR1Initial > 6, rkipR1Initial <= 8)
        rkipR1InitialInterval6 = And(rkipR1Initial > 8, rkipR1Initial <= 16)
        rkipR1InitialConstraints = Or(rkipR1InitialInterval1, rkipR1InitialInterval2, rkipR1InitialInterval3,
                                      rkipR1InitialInterval4, rkipR1InitialInterval5, rkipR1InitialInterval6)

        rkipR1FinalInterval1 = (rkipR1Final == 0)
        rkipR1FinalInterval2 = And(rkipR1Final > 0, rkipR1Final <= 2)
        rkipR1FinalInterval3 = And(rkipR1Final > 2, rkipR1Final <= 4)
        rkipR1FinalInterval4 = And(rkipR1Final > 4, rkipR1Final <= 6)
        rkipR1FinalInterval5 = And(rkipR1Final > 6, rkipR1Final <= 8)
        rkipR1FinalInterval6 = And(rkipR1Final > 8, rkipR1Final <= 16)
        rkipR1FinalConstraints = Or(rkipR1FinalInterval1, rkipR1FinalInterval2, rkipR1FinalInterval3,
                                    rkipR1FinalInterval4, rkipR1FinalInterval5, rkipR1FinalInterval6)

        # raf1rkip: ZERO, S0E40, S40E60, S60E80, S80E100, S100E140
        raf1rkipR1InitialInterval1 = (raf1rkipR1Initial == 0)
        raf1rkipR1InitialInterval2 = And(raf1rkipR1Initial > 0, raf1rkipR1Initial <= 40)
        raf1rkipR1InitialInterval3 = And(raf1rkipR1Initial > 40, raf1rkipR1Initial <= 60)
        raf1rkipR1InitialInterval4 = And(raf1rkipR1Initial > 60, raf1rkipR1Initial <= 80)
        raf1rkipR1InitialInterval5 = And(raf1rkipR1Initial > 80, raf1rkipR1Initial <= 100)
        raf1rkipR1InitialInterval6 = And(raf1rkipR1Initial > 100, raf1rkipR1Initial <= 140)
        raf1rkipR1InitialConstraints = Or(raf1rkipR1InitialInterval1, raf1rkipR1InitialInterval2,
                                          raf1rkipR1InitialInterval3, raf1rkipR1InitialInterval4,
                                          raf1rkipR1InitialInterval5, raf1rkipR1InitialInterval6)

        raf1rkipR1FinalInterval1 = (raf1rkipR1Final == 0)
        raf1rkipR1FinalInterval2 = And(raf1rkipR1Final > 0, raf1rkipR1Final <= 40)
        raf1rkipR1FinalInterval3 = And(raf1rkipR1Final > 40, raf1rkipR1Final <= 60)
        raf1rkipR1FinalInterval4 = And(raf1rkipR1Final > 60, raf1rkipR1Final <= 80)
        raf1rkipR1FinalInterval5 = And(raf1rkipR1Final > 80, raf1rkipR1Final <= 100)
        raf1rkipR1FinalInterval6 = And(raf1rkipR1Final > 100, raf1rkipR1Final <= 140)
        raf1rkipR1FinalConstraints = Or(raf1rkipR1FinalInterval1, raf1rkipR1FinalInterval2, raf1rkipR1FinalInterval3,
                                        raf1rkipR1FinalInterval4, raf1rkipR1FinalInterval5, raf1rkipR1FinalInterval6)

        # Calculate the product of the reaction
        rate1 = 0.5228
        product1 = If(raf1R1Initial < rkipR1Initial, raf1R1Initial * rate1, rkipR1Initial * rate1)
        reaction1 = And((raf1R1Final == raf1R1Initial - product1),
                     (rkipR1Final == rkipR1Initial - product1),
                     (raf1rkipR1Final == raf1rkipR1Initial + product1 * 2))

        # Add the interval constraints to the solver
        SMTsolver.add(raf1R1InitialConstraints)
        SMTsolver.add(raf1R1FinalConstraints)
        SMTsolver.add(rkipR1InitialConstraints)
        SMTsolver.add(rkipR1FinalConstraints)
        SMTsolver.add(raf1rkipR1InitialConstraints)
        SMTsolver.add(raf1rkipR1FinalConstraints)

        # Add the product and reaction constraints to the solver to simulate the reaction
        SMTsolver.add(reaction1)

    if k_bound >= 2:
        # Reaction 2: raf1rkip + erkpp = raf1rkiperkpp
        # Rate of Reaction: 0.62255
        # Ranges: 40-140, 100-1800, 200-500

        # Add the transition link: raf1rkip also appears in reaction 1
        SMTsolver.add(raf1rkipR2Initial == raf1rkipR1Final)

        # Add constraints to represent each chemical interval
        # raf1rkip: ZERO, S0E40, S40E60, S60E80, S80E100, S100E140
        raf1rkipR2FinalInterval1 = (raf1rkipR2Final == 0)
        raf1rkipR2FinalInterval2 = And(raf1rkipR2Final > 0, raf1rkipR2Final <= 40)
        raf1rkipR2FinalInterval3 = And(raf1rkipR2Final > 40, raf1rkipR2Final <= 60)
        raf1rkipR2FinalInterval4 = And(raf1rkipR2Final > 60, raf1rkipR2Final <= 80)
        raf1rkipR2FinalInterval5 = And(raf1rkipR2Final > 80, raf1rkipR2Final <= 100)
        raf1rkipR2FinalInterval6 = And(raf1rkipR2Final > 100, raf1rkipR2Final <= 140)
        raf1rkipR2FinalConstraints = Or(raf1rkipR2FinalInterval1, raf1rkipR2FinalInterval2, raf1rkipR2FinalInterval3,
                                        raf1rkipR2FinalInterval4, raf1rkipR2FinalInterval5, raf1rkipR2FinalInterval6)

        # erkpp: ZERO, S0E100, S100E440, S440E780, S780E1120, S1120E1800
        erkppR2InitialInterval1 = (erkppR2Initial == 0)
        erkppR2InitialInterval2 = And(erkppR2Initial > 0, erkppR2Initial <= 100)
        erkppR2InitialInterval3 = And(erkppR2Initial > 100, erkppR2Initial <= 440)
        erkppR2InitialInterval4 = And(erkppR2Initial > 440, erkppR2Initial <= 780)
        erkppR2InitialInterval5 = And(erkppR2Initial > 780, erkppR2Initial <= 1120)
        erkppR2InitialInterval6 = And(erkppR2Initial > 1120, erkppR2Initial <= 1800)
        erkppR2InitialConstraints = Or(erkppR2InitialInterval1, erkppR2InitialInterval2, erkppR2InitialInterval3,
                                       erkppR2InitialInterval4, erkppR2InitialInterval5, erkppR2InitialInterval6)

        erkppR2FinalInterval1 = (erkppR2Final == 0)
        erkppR2FinalInterval2 = And(erkppR2Final > 0, erkppR2Final <= 100)
        erkppR2FinalInterval3 = And(erkppR2Final > 100, erkppR2Final <= 440)
        erkppR2FinalInterval4 = And(erkppR2Final > 440, erkppR2Final <= 780)
        erkppR2FinalInterval5 = And(erkppR2Final > 780, erkppR2Final <= 1120)
        erkppR2FinalInterval6 = And(erkppR2Final > 1120, erkppR2Final <= 1800)
        erkppR2FinalConstraints = Or(erkppR2FinalInterval1, erkppR2FinalInterval2, erkppR2FinalInterval3,
                                     erkppR2FinalInterval4, erkppR2FinalInterval5, erkppR2FinalInterval6)

        # raf1rkiperkpp: ZERO, S0E200, S200E260, S260E320, S320E380, S380E500
        raf1rkiperkppR2InitialInterval1 = (raf1rkiperkppR2Initial == 0)
        raf1rkiperkppR2InitialInterval2 = And(raf1rkiperkppR2Initial > 0, raf1rkiperkppR2Initial <= 200)
        raf1rkiperkppR2InitialInterval3 = And(raf1rkiperkppR2Initial > 200, raf1rkiperkppR2Initial <= 260)
        raf1rkiperkppR2InitialInterval4 = And(raf1rkiperkppR2Initial > 260, raf1rkiperkppR2Initial <= 320)
        raf1rkiperkppR2InitialInterval5 = And(raf1rkiperkppR2Initial > 320, raf1rkiperkppR2Initial <= 380)
        raf1rkiperkppR2InitialInterval6 = And(raf1rkiperkppR2Initial > 380, raf1rkiperkppR2Initial <= 500)
        raf1rkiperkppR2InitialConstraints = Or(raf1rkiperkppR2InitialInterval1, raf1rkiperkppR2InitialInterval2,
                                               raf1rkiperkppR2InitialInterval3, raf1rkiperkppR2InitialInterval4,
                                               raf1rkiperkppR2InitialInterval5, raf1rkiperkppR2InitialInterval6)

        raf1rkiperkppR2FinalInterval1 = (raf1rkiperkppR2Final == 0)
        raf1rkiperkppR2FinalInterval2 = And(raf1rkiperkppR2Final > 0, raf1rkiperkppR2Final <= 200)
        raf1rkiperkppR2FinalInterval3 = And(raf1rkiperkppR2Final > 200, raf1rkiperkppR2Final <= 260)
        raf1rkiperkppR2FinalInterval4 = And(raf1rkiperkppR2Final > 260, raf1rkiperkppR2Final <= 320)
        raf1rkiperkppR2FinalInterval5 = And(raf1rkiperkppR2Final > 320, raf1rkiperkppR2Final <= 380)
        raf1rkiperkppR2FinalInterval6 = And(raf1rkiperkppR2Final > 380, raf1rkiperkppR2Final <= 500)
        raf1rkiperkppR2FinalConstraints = Or(raf1rkiperkppR2FinalInterval1, raf1rkiperkppR2FinalInterval2,
                                             raf1rkiperkppR2FinalInterval3, raf1rkiperkppR2FinalInterval4,
                                             raf1rkiperkppR2FinalInterval5, raf1rkiperkppR2FinalInterval6)

        # Calculate the product of the reaction
        rate2 = 0.62255
        product2 = If(raf1rkipR2Initial < erkppR2Initial, raf1rkipR2Initial * rate2, erkppR2Initial * rate2)
        reaction2 = And((raf1rkipR2Final == raf1rkipR2Initial - product2),
                     (erkppR2Final == erkppR2Initial - product2),
                     (raf1rkiperkppR2Final == raf1rkiperkppR2Initial + product2 * 2))

        # Add the interval constraints to the solver
        SMTsolver.add(raf1rkipR2FinalConstraints)
        SMTsolver.add(erkppR2InitialConstraints)
        SMTsolver.add(erkppR2FinalConstraints)
        SMTsolver.add(raf1rkiperkppR2InitialConstraints)
        SMTsolver.add(raf1rkiperkppR2FinalConstraints)

        # Add the product and reaction constraints to the solver to simulate the reaction
        SMTsolver.add(reaction2)

    if k_bound >= 3:
        # Reaction 3: raf1rkiperkpp = raf1 + erkp + rkipp
        # Rate of Reaction: 0.0315
        # Ranges: 200-500, 200-700, 10-50, 200-220

        # Add the transition links: raf1rkiperkpp also appears in reaction 2, and raf1 also appears in reaction 1
        SMTsolver.add(raf1rkiperkppR3Initial == raf1rkiperkppR2Final)
        SMTsolver.add(raf1R3Initial == raf1R1Final)

        # raf1rkiperkpp: ZERO, S0E200, S200E260, S260E320, S320E380, S380E500
        raf1rkiperkppR3FinalInterval1 = (raf1rkiperkppR3Final == 0)
        raf1rkiperkppR3FinalInterval2 = And(raf1rkiperkppR3Final > 0, raf1rkiperkppR3Final <= 200)
        raf1rkiperkppR3FinalInterval3 = And(raf1rkiperkppR3Final > 200, raf1rkiperkppR3Final <= 260)
        raf1rkiperkppR3FinalInterval4 = And(raf1rkiperkppR3Final > 260, raf1rkiperkppR3Final <= 320)
        raf1rkiperkppR3FinalInterval5 = And(raf1rkiperkppR3Final > 320, raf1rkiperkppR3Final <= 380)
        raf1rkiperkppR3FinalInterval6 = And(raf1rkiperkppR3Final > 380, raf1rkiperkppR3Final <= 500)
        raf1rkiperkppR3FinalConstraints = Or(raf1rkiperkppR3FinalInterval1, raf1rkiperkppR3FinalInterval2,
                                             raf1rkiperkppR3FinalInterval3, raf1rkiperkppR3FinalInterval4,
                                             raf1rkiperkppR3FinalInterval5, raf1rkiperkppR3FinalInterval6)

        # raf1: ZERO, S0E200, S200E300, S300E400, S400E500, S500E700
        raf1R3FinalInterval1 = (raf1R3Final == 0)
        raf1R3FinalInterval2 = And(raf1R3Final > 0, raf1R3Final <= 200)
        raf1R3FinalInterval3 = And(raf1R3Final > 200, raf1R3Final <= 300)
        raf1R3FinalInterval4 = And(raf1R3Final > 300, raf1R3Final <= 400)
        raf1R3FinalInterval5 = And(raf1R3Final > 400, raf1R3Final <= 500)
        raf1R3FinalInterval6 = And(raf1R3Final > 500, raf1R3Final <= 700)
        raf1R3FinalConstraints = Or(raf1R3FinalInterval1, raf1R3FinalInterval2, raf1R3FinalInterval3,
                                    raf1R3FinalInterval4, raf1R3FinalInterval5, raf1R3FinalInterval6)

        # erkp: ZERO, S0E10, S10E18, S18E26, S26E34, S34E50
        erkpR3InitialInterval1 = (erkpR3Initial == 0)
        erkpR3InitialInterval2 = And(erkpR3Initial > 0, erkpR3Initial <= 10)
        erkpR3InitialInterval3 = And(erkpR3Initial > 10, erkpR3Initial <= 18)
        erkpR3InitialInterval4 = And(erkpR3Initial > 18, erkpR3Initial <= 26)
        erkpR3InitialInterval5 = And(erkpR3Initial > 26, erkpR3Initial <= 34)
        erkpR3InitialInterval6 = And(erkpR3Initial > 34, erkpR3Initial <= 50)
        erkpR3InitialConstraints = Or(erkpR3InitialInterval1, erkpR3InitialInterval2, erkpR3InitialInterval3,
                                      erkpR3InitialInterval4, erkpR3InitialInterval5, erkpR3InitialInterval6)

        erkpR3FinalInterval1 = (erkpR3Final == 0)
        erkpR3FinalInterval2 = And(erkpR3Final > 0, erkpR3Final <= 10)
        erkpR3FinalInterval3 = And(erkpR3Final > 10, erkpR3Final <= 18)
        erkpR3FinalInterval4 = And(erkpR3Final > 18, erkpR3Final <= 26)
        erkpR3FinalInterval5 = And(erkpR3Final > 26, erkpR3Final <= 34)
        erkpR3FinalInterval6 = And(erkpR3Final > 34, erkpR3Final <= 50)
        erkpR3FinalConstraints = Or(erkpR3FinalInterval1, erkpR3FinalInterval2, erkpR3FinalInterval3,
                                    erkpR3FinalInterval4, erkpR3FinalInterval5, erkpR3FinalInterval6)

        # rkipp: ZERO, S0E200, S200E204, S204E208, S208E212, S212E220
        rkippR3InitialInterval1 = (rkippR3Initial == 0)
        rkippR3InitialInterval2 = And(rkippR3Initial > 0, rkippR3Initial <= 200)
        rkippR3InitialInterval3 = And(rkippR3Initial > 200, rkippR3Initial <= 204)
        rkippR3InitialInterval4 = And(rkippR3Initial > 204, rkippR3Initial <= 208)
        rkippR3InitialInterval5 = And(rkippR3Initial > 208, rkippR3Initial <= 212)
        rkippR3InitialInterval6 = And(rkippR3Initial > 212, rkippR3Initial <= 220)
        rkippR3InitialConstraints = Or(rkippR3InitialInterval1, rkippR3InitialInterval2, rkippR3InitialInterval3,
                                       rkippR3InitialInterval4, rkippR3InitialInterval5, rkippR3InitialInterval6)

        rkippR3FinalInterval1 = (rkippR3Final == 0)
        rkippR3FinalInterval2 = And(rkippR3Final > 0, rkippR3Final <= 200)
        rkippR3FinalInterval3 = And(rkippR3Final > 200, rkippR3Final <= 204)
        rkippR3FinalInterval4 = And(rkippR3Final > 204, rkippR3Final <= 208)
        rkippR3FinalInterval5 = And(rkippR3Final > 208, rkippR3Final <= 212)
        rkippR3FinalInterval6 = And(rkippR3Final > 212, rkippR3Final <= 220)
        rkippR3FinalConstraints = Or(rkippR3FinalInterval1, rkippR3FinalInterval2, rkippR3FinalInterval3,
                                     rkippR3FinalInterval4, rkippR3FinalInterval5, rkippR3FinalInterval6)

        # Calculate the product of the reaction
        rate3 = 0.0315
        product3 = (raf1rkiperkppR3Initial * rate3)
        reaction3 = And((raf1rkiperkppR3Final == raf1rkiperkppR3Initial - product3),
                     (raf1R3Final == raf1R3Initial + product3 / 3),
                     (erkpR3Final == erkpR3Initial + product3 / 3),
                     (rkippR3Final == rkippR3Initial + product3 / 3))

        # Add the interval constraints to the solver
        SMTsolver.add(raf1rkiperkppR3FinalConstraints)
        SMTsolver.add(raf1R3FinalConstraints)
        SMTsolver.add(erkpR3InitialConstraints)
        SMTsolver.add(erkpR3FinalConstraints)
        SMTsolver.add(rkippR3InitialConstraints)
        SMTsolver.add(rkippR3FinalConstraints)

        # Add the product and reaction constraints to the solver to simulate the reaction
        SMTsolver.add(reaction3)

    if k_bound >= 4:
        # Reaction 4: rkipp + rp -> rkipprp
        # Rate of Reaction: 0.91878
        # Ranges: 200-220, 600-1800, 100-500

        # Add the transition link: rkipp also appears in reaction 3
        SMTsolver.add(rkippR4Initial == rkippR3Final)

        # rkipp: ZERO, S0E200, S200E204, S204E208, S208E212, S212E220
        rkippR4FinalInterval1 = (rkippR4Final == 0)
        rkippR4FinalInterval2 = And(rkippR4Final > 0, rkippR4Final <= 200)
        rkippR4FinalInterval3 = And(rkippR4Final > 200, rkippR4Final <= 204)
        rkippR4FinalInterval4 = And(rkippR4Final > 204, rkippR4Final <= 208)
        rkippR4FinalInterval5 = And(rkippR4Final > 208, rkippR4Final <= 212)
        rkippR4FinalInterval6 = And(rkippR4Final > 212, rkippR4Final <= 220)
        rkippR4FinalConstraints = Or(rkippR4FinalInterval1, rkippR4FinalInterval2, rkippR4FinalInterval3,
                                     rkippR4FinalInterval4, rkippR4FinalInterval5, rkippR4FinalInterval6)

        # rp: ZERO, S0E600, S600E840, S840E1080, S1080E1320, S1320E1800
        rpR4InitialInterval1 = (rpR4Initial == 0)
        rpR4InitialInterval2 = And(rpR4Initial > 0, rpR4Initial <= 600)
        rpR4InitialInterval3 = And(rpR4Initial > 600, rpR4Initial <= 840)
        rpR4InitialInterval4 = And(rpR4Initial > 840, rpR4Initial <= 1080)
        rpR4InitialInterval5 = And(rpR4Initial > 1080, rpR4Initial <= 1320)
        rpR4InitialInterval6 = And(rpR4Initial > 1320, rpR4Initial <= 1800)
        rpR4InitialConstraints = Or(rpR4InitialInterval1, rpR4InitialInterval2, rpR4InitialInterval3,
                                    rpR4InitialInterval4, rpR4InitialInterval5, rpR4InitialInterval6)

        rpR4FinalInterval1 = (rpR4Final == 0)
        rpR4FinalInterval2 = And(rpR4Final > 0, rpR4Final <= 600)
        rpR4FinalInterval3 = And(rpR4Final > 600, rpR4Final <= 840)
        rpR4FinalInterval4 = And(rpR4Final > 840, rpR4Final <= 1080)
        rpR4FinalInterval5 = And(rpR4Final > 1080, rpR4Final <= 1320)
        rpR4FinalInterval6 = And(rpR4Final > 1320, rpR4Final <= 1800)
        rpR4FinalConstraints = Or(rpR4FinalInterval1, rpR4FinalInterval2, rpR4FinalInterval3, rpR4FinalInterval4,
                                  rpR4FinalInterval5, rpR4FinalInterval6)

        # rkipprp: ZERO, S0E100, S100E180, S180E260, S260E340, S340E500
        rkipprpR4InitialInterval1 = (rkipprpR4Initial == 0)
        rkipprpR4InitialInterval2 = And(rkipprpR4Initial > 0, rkipprpR4Initial <= 100)
        rkipprpR4InitialInterval3 = And(rkipprpR4Initial > 100, rkipprpR4Initial <= 180)
        rkipprpR4InitialInterval4 = And(rkipprpR4Initial > 180, rkipprpR4Initial <= 260)
        rkipprpR4InitialInterval5 = And(rkipprpR4Initial > 260, rkipprpR4Initial <= 340)
        rkipprpR4InitialInterval6 = And(rkipprpR4Initial > 340, rkipprpR4Initial <= 500)
        rkipprpR4InitialConstraints = Or(rkipprpR4InitialInterval1, rkipprpR4InitialInterval2,
                                         rkipprpR4InitialInterval3, rkipprpR4InitialInterval4,
                                         rkipprpR4InitialInterval5, rkipprpR4InitialInterval6)

        rkipprpR4FinalInterval1 = (rkipprpR4Final == 0)
        rkipprpR4FinalInterval2 = And(rkipprpR4Final > 0, rkipprpR4Final <= 100)
        rkipprpR4FinalInterval3 = And(rkipprpR4Final > 100, rkipprpR4Final <= 180)
        rkipprpR4FinalInterval4 = And(rkipprpR4Final > 180, rkipprpR4Final <= 260)
        rkipprpR4FinalInterval5 = And(rkipprpR4Final > 260, rkipprpR4Final <= 340)
        rkipprpR4FinalInterval6 = And(rkipprpR4Final > 340, rkipprpR4Final <= 500)
        rkipprpR4FinalConstraints = Or(rkipprpR4FinalInterval1, rkipprpR4FinalInterval2, rkipprpR4FinalInterval3,
                                       rkipprpR4FinalInterval4, rkipprpR4FinalInterval5, rkipprpR4FinalInterval6)

        # Reaction 4: rkipp + rp -> rkipprp
        # Calculate the product of the reaction
        rate4 = 0.91878
        product4 = If(rkippR4Initial < rpR4Initial, rkippR4Initial * rate4, rpR4Initial * rate4)
        reaction4 = And((rkippR4Final == rkippR4Initial - product4),
                     (rpR4Final == rpR4Initial - product4),
                     (rkipprpR4Final == rkipprpR4Initial + product4 * 2))

        # Add the interval constraints to the solver
        SMTsolver.add(rkippR4FinalConstraints)
        SMTsolver.add(rpR4InitialConstraints)
        SMTsolver.add(rpR4FinalConstraints)
        SMTsolver.add(rkipprpR4InitialConstraints)
        SMTsolver.add(rkipprpR4FinalConstraints)

        # Add the product and reaction constraints to the solver to simulate the reaction
        SMTsolver.add(reaction4)

# ***********************************************

k_bound = int(input("Enter BMC Bound: "))

# Build the model using a user-define k value
build_model(solver, k_bound)

# ***********************************************

print("\nBOUNDED MODEL CHECKING QUERIES:")

print("\nQuery 1: raf1 = S500E700")
# Save the state of the solver at this point
solver.push()

# Initial value I: raf1 starts in S500E700 interval
Query1_I = And(raf1R1Initial > 500, raf1R1Initial <= 700)
solver.add(Query1_I)

# The property P: does raf1 fall into interval S500E700 at any point?
# Before reaction 1
Query1_P0 = And(raf1R1Initial > 500, raf1R1Initial <= 700)

# After reaction 1
Query1_P1 = And(raf1R1Final > 500, raf1R1Final <= 700)

# After reaction 3
Query1_P3 = And(raf1R3Final > 500, raf1R3Final <= 700)

# Add the appropriate property dependent on the BMC bound
if k_bound >= 3:
    Query1_P = Or(Query1_P0, Query1_P1, Query1_P3)
elif k_bound == 2 or k_bound == 1:
    Query1_P = Or(Query1_P0, Query1_P1)
else:
    Query1_P = Query1_P0

solver.add(Not(Query1_P))

if solver.check() == sat:
    print("Result: SAT (Counterexample Found)")
    print("The property (raf1 = S500E700) does not hold.")
    print(F"Violating model: {solver.model()}")

else:
    print("Result: UNSAT (No Counterexamples Found)")
    print("The property (raf1 = S500E700) holds for all possibilities.")
print()
# Restore the state of the original solver
solver.pop()

print("\nQuery 2: raf1 = S500E700 AND rkip = ZERO")
# Push
solver.push()

# Initial value I: raf1 starts in S500E700 interval and rkip starts in the S8E16 interval
Query2_I = And(
    And(raf1R1Initial > 500, raf1R1Initial <= 700),
    And(rkipR1Initial > 8, rkipR1Initial <= 16)
)
solver.add(Query2_I)

# The property P: at any point, does raf1 fall into interval S500E700 while rkip is ZERO?
# Before reaction 1
Query2_P0 = And(And(raf1R1Initial > 500, raf1R1Initial <= 700), And(rkipR1Initial == 0))

# After reaction 1
Query2_P1 = And(And(raf1R1Final > 500, raf1R1Final <= 700), And(rkipR1Final == 0))

# After reaction 3
Query2_P3 = And(And(raf1R3Final > 500, raf1R3Final <= 700), And(rkipR1Final == 0))

# Add the appropriate property dependent on the BMC bound
if k_bound >= 3:
    Query2_P = Or(Query2_P0, Query2_P1, Query2_P3)
elif k_bound == 2 or k_bound == 1:
    Query2_P = Or(Query2_P0, Query2_P1)
else:
    Query2_P = Query2_P0

solver.add(Not(Query2_P))

if solver.check() == sat:
    print("Result: SAT (Counterexample Found)")
    print("The property (raf1 = S500E700 AND rkip = ZERO) does not hold.")
    print(F"Violating model: {solver.model()}")

else:
    print("Result: UNSAT (No Counterexamples Found)")
    print("The property (raf1 = S500E700 AND rkip = ZERO) holds for all possibilities.")
print()

# Restore the state of the original solver
solver.pop()

print("\nQuery 3: raf1 = S500E700 AND rkip = S6E8")
# Push
solver.push()

# Initial value I: raf1 starts in S500E700 interval and rkip starts in the S8E16 interval
Query3_I = And(
    And(raf1R1Initial > 500, raf1R1Initial <= 700),
    And(rkipR1Initial > 8, rkipR1Initial <= 16)
)
solver.add(Query3_I)

# The property P: at any point, does raf1 fall into interval S500E700 while rkip is S6E8?
# Before reaction 1
Query3_P0 = And(And(raf1R1Initial > 500, raf1R1Initial <= 700), And(rkipR1Initial >  6, rkipR1Initial <= 8))

# After reaction 1
Query3_P1 = And(And(raf1R1Final > 500, raf1R1Final <= 700), And(rkipR1Final >  6, rkipR1Final <= 8))

# After reaction 3
Query3_P3 = And(And(raf1R3Final > 500, raf1R3Final <= 700), And(rkipR1Final >  6, rkipR1Final <= 8))

# Add the appropriate property dependent on the BMC bound
if k_bound >= 3:
    Query3_P = Or(Query3_P0, Query3_P1, Query3_P3)
elif k_bound == 2 or k_bound == 1:
    Query3_P = Or(Query3_P0, Query3_P1)
else:
    Query3_P = Query3_P0

solver.add(Not(Query3_P))

if solver.check() == sat:
    print("Result: SAT (Counterexample Found)")
    print("The property (raf1 = S500E700 AND rkip = S6E8) does not hold.")
    print(F"Violating model: {solver.model()}")

else:
    print("Result: UNSAT (No Counterexamples Found)")
    print("The property (raf1 = S500E700 AND rkip = S6E8) holds for all possibilities.")
print()

# Restore the state of the original solver
solver.pop()