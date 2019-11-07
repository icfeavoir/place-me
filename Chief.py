from Group import *
from GA import *
from Constraint import *
from Server import *
from dotenv import load_dotenv
import os
import time


class Chief:
    def __init__(self):
        self.plan = None
        self.constraints = None
        self.groups = None

        self.server = None
        self.conn = None

        load_dotenv()
        self.NB_GENERATION = int(os.getenv("NB_GENERATION"))
        self.NB_PLANS = int(os.getenv("NB_PLANS"))
        self.PROB_MUTATIONS = float(os.getenv("PROB_MUTATIONS"))
        self.NB_REPRODUCTION = round(self.NB_PLANS * float(os.getenv("NB_REPRODUCTION")))

        self.PORT = float(os.getenv("PORT"))

    def start(self, test_mode = False):
        if test_mode:
            return self.test_mode()
        else:
            self.server = Server(self, self.PORT)
            self.server.start_server()

    def json_to_data(self, data, conn):
        self.conn = conn

        # init data
        self.plan = []
        self.constraints = []
        self.groups = []

        width = data["width"]
        height = data["height"]
        forbidden_seats = data["forbidden_seats"]
        for line in range (height - 1):
            self.plan.append([])
            for cell in range (width - 1):
                forbid = any(fseat["line"] == line and fseat["cell"] == cell for fseat in forbidden_seats)
                self.plan[line].append(0 if forbid else 1)

        groups = data["groups"]
        for group in groups:
            self.groups.append(Group(group["name"], group["number"], None, 0))

        self.lets_go()

    def lets_go(self):
        Plan.grid = self.plan
        Plan.groups = self.groups
        Plan.constraints = self.constraints

        print(
            "GA STARTS!\n" +
            "NB_GENERATION = " + str(self.NB_GENERATION ) + " - " +
            "NB_PLANS = " + str(self.NB_PLANS ) + " - " +
            "PROB_MUTATIONS = " + str(self.PROB_MUTATIONS ) + " - " +
            "NB_REPRODUCTION = " + str(self.NB_REPRODUCTION )
        )


        time_start = time.time()

        # INIT
        list_plans = []
        ' on crée des plans random, on calcule les scores '
        for i in range(self.NB_PLANS):
            plan = Plan()
            plan.gen_random()
            plan.calculate_score()
            list_plans.append(plan)
        ga = GA(list_plans, self.NB_REPRODUCTION, self.PROB_MUTATIONS)

        for i in range(self.NB_GENERATION):
            ga.reproduce()
            ga.keep_only(self.NB_PLANS)
            ga.mutate()

        ga.sort_plans()

        if self.conn is not None:
            self.conn.send(str.encode(str(ga.list_plans[0])))

        time_end = time.time()

        best_plan = ga.list_plans[0]
        # print(best_plan)
        # print("[SCORE: " + str(best_plan.score) + "]")
        # print("EXECUTED IN " + str(round(time_end - time_start, 3)) + " seconds")

        return best_plan, round(time_end - time_start, 3)

    def test_mode(self):
        # le plan
        self.plan = [
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
        # Les contraintes
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
        self.constraints = [
            ct_p_rang,
            ct_milieu,
        ]

        # les groupes de personnes
        self.groups = [
            Group("Madi.L", 5, ct_p_rang, "*"),
            Group("Leco.A", 6, None, 0),
            Group("Maingu", 2, None, 0),
            Group("Bour.R", 2, None, 0),
            Group("Coll.J", 8, None, 0),
            Group("Meun.V", 16, None, 0),
            Group("Leme.H", 3, None, 0),
            Group("Vall.M", 2, None, 0),
            Group("Lero.E", 2, None, 0),
            Group("Laur.T", 8, None, 0),
            # Group("Jupin", 2, None, 0),
            # Group("Pean.A", 2, None, 0),
            # Group("Bett.A", 9, None, 0),
            # Group("Les vi  ", 33, None, 0),
            # Group("Pins.V  ", 10, None, 0),
            # Group("Pott.N", 2, None, 0),
            # Group("Remi p", 3, None, 0),
            # Group("Epro.I", 6, None, 0),
            # Group("Doue.K", 1, None, 0),
            # Group("Dilis", 3, None, 0),
            # Group("Delcou", 4, None, 0),
            # Group("Epro.M", 5, None, 0),
            # Group("Gibon", 6, None, 0),
            # Group("Lang.P  ", 19, None, 0),
            # Group("Rondea", 1, None, 0),
            # Group("Jarr.V", 2, None, 0),
            # Group("Dane.D", 2, None, 0),
            # Group("Techer", 4, None, 0),
            # Group("Pier.J", 5, None, 0),
            # Group("Pillai", 7, None, 0),
            # Group("Less.B", 1, None, 0),
            # Group("Yver.M", 3, None, 0),
        ]

        return self.lets_go()
