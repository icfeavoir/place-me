from Group import *
from GA import *
from Constraint import *
from dotenv import load_dotenv
import os
import time

load_dotenv()

NB_GENERATION = int(os.getenv("NB_GENERATION"))
NB_PLANS = int(os.getenv("NB_PLANS"))
PROB_MUTATIONS = float(os.getenv("PROB_MUTATIONS"))
NB_REPRODUCTION = round(NB_PLANS * 0.2)

if __name__ == '__main__':
    ' le plan '
    grid = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
    ]

    ' Les contraintes'
    ct_p_rang = Constraint("p_rang")
    ct_p_rang.set_concerned_seats([
        [8, 0],
        [8, 1],
        [8, 2],
        [8, 3],
        [8, 4],
        [8, 5],
        [8, 6],
        [8, 7],
        [8, 8],
        [8, 9],
        [8, 10],
        [8, 12],
        [8, 12],
        [8, 13],
        [8, 14],
        [8, 15],
        [8, 16],
        [8, 17],
        [8, 18],
        [8, 19],
        [8, 20],
        [8, 21],
        [8, 22],
        [8, 23],
    ])
    ct_milieu = Constraint("milieu")
    ct_milieu.set_concerned_seats([
        [3, 0],
        [3, 1],
        [3, 2],
    ])
    constraints = [
        ct_p_rang,
        ct_milieu,
    ]

    ' les groupes de personnes '
    groups = [
        Group("Madi.L - 5     ", 5, ct_p_rang, "*"),
        # Group("Leco.A - 6   ", 6, 0, 0),
        # Group("Maingu - 2   ", 2, 0, 0),
        # Group("Bour.R - 2   ", 2, 0, 0),
        # Group("Coll.J - 8   ", 8, 0, 0),
        # Group("Meun.V - 16  ", 16, 0, 0),
        # Group("Leme.H - 3   ", 3, 0, 0),
        # Group("Vall.M - 2   ", 2, 0, 0),
        # Group("Lero.E - 2   ", 2, 0, 0),
        # Group("Laur.T - 8   ", 8, 0, 0),
        # Group("Jupin - 2    ", 2, 0, 0),
        # Group("Pean.A - 2   ", 2, 0, 0),
        # Group("Bett.A - 9   ", 9, 0, 0),
        # Group("Les vi  - 33 ", 33, 0, 0),
        # Group("Pins.V - 10  ", 10, 0, 0),
        # Group("Pott.N - 2   ", 2, 0, 0),
        # Group("Remi p - 3   ", 3, 0, 0),
        # Group("Epro.I - 6   ", 6, 0, 0),
        # Group("Doue.K - 1   ", 1, 0, 0),
        # Group("Dilis - 3    ", 3, 0, 0),
        # Group("Delcou - 4   ", 4, 0, 0),
        # Group("Epro.M - 5   ", 5, 0, 0),
        # Group("Gibon - 6    ", 6, 0, 0),
        # Group("Lang.P - 19  ", 19, 0, 0),
        # Group("Rondea - 1   ", 1, 0, 0),
        # Group("Jarr.V - 2   ", 2, 0, 0),
        # Group("Dane.D - 2   ", 2, 0, 0),
        # Group("Techer - 4   ", 4, 0, 0),
        # Group("Pier.J - 5   ", 5, 0, 0),
        # Group("Pillai - 7   ", 7, 0, 0),
        # Group("Less.B - 1   ", 1, 0, 0),
        # Group("Yver.M - 3   ", 3, 0, 0),
    ]

    Plan.grid = grid
    Plan.groups = groups
    Plan.constraints = constraints

    time_start = time.time()

    # INIT
    listPlans = []
    ' on crée des plans random, on calcule les scores '
    for i in range(NB_PLANS):
        plan = Plan()
        plan.gen_random()
        plan.calculate_score()
        listPlans.append(plan)
    ga = GA(listPlans, NB_REPRODUCTION, PROB_MUTATIONS)

    for i in range(NB_GENERATION):
        ga.reproduce()
        ga.keep_only(NB_PLANS)
        ga.mutate()

    print("DONE")
    ga.sort_plans()
    print(ga.listPlans[0])

    time_end = time.time()

    print("EXECUTED IN " + str(round(time_end - time_start, 3)) + " seconds")
