import copy
from Plan import *


class GA:

    def __init__(self, list_plans, nb_reproduction, prob_mutation):
        self.listPlans = list_plans
        self.nb_reproduction = nb_reproduction
        self.prob_mutation = prob_mutation

    def __str__(self):
        res = ""
        for plan in self.listPlans:
            res += str(plan) + "\n"
        return res

    def sort_plans(self):
        self.listPlans.sort(key=lambda x: x.score, reverse=True)

    def roulette_wheel_selection(self):
        # Technique de sélection de plan.
        # Chaque plan de la liste peut être choisi, mais plus son score est bon, plus sa prob d'être
        # choisi est grande.

        self.sort_plans()

        somme_score = 0
        for plan in self.listPlans:
            somme_score += plan.score
        choosed_score = random.randint(0, somme_score)
        score_counter = 0
        for plan in self.listPlans:
            score_counter += plan.score
            if score_counter >= choosed_score:
                return plan

    def reproduce(self):
        for i in range(self.nb_reproduction):
            ' on prend une partie mère et une partie père pour reformer un plan'
            new_plan = Plan()
            mother = self.roulette_wheel_selection()
            father = self.roulette_wheel_selection()
            new_plan.create_from_parents(copy.deepcopy(mother), copy.deepcopy(father))
            new_plan.correct_placement()
            self.listPlans.append(new_plan)

    def mutate(self):
        for plan in self.listPlans:
            r = random.randint(0, 100) / 100
            if r < self.prob_mutation:
                # if lucky we mutate 2 seats
                random_line_1 = random.randint(0, len(plan.placement) - 1)
                random_cell_1 = random.randint(0, len(plan.placement[random_line_1]) - 1)
                name1 = plan.get_people_at(random_line_1, random_cell_1)
                random_line_2 = random.randint(0, len(plan.placement) - 1)
                random_cell_2 = random.randint(0, len(plan.placement[random_line_2]) - 1)
                name2 = plan.get_people_at(random_line_2, random_cell_2)
                plan.set_people_at(random_line_1, random_cell_1, name2)
                plan.set_people_at(random_line_2, random_cell_2, name1)
                plan.calculate_score()

    def keep_only(self, nb):
        self.sort_plans()
        self.listPlans = self.listPlans[:nb]
