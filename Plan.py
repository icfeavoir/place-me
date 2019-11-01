import random


class Plan:

    grid = []
    groups = []
    constraints = []

    def __str__(self):
        res = "[SCORE: " + str(self.score) + "]\n"
        for line_number, cells in enumerate(self.placement):
            for cell_number, people in enumerate(cells):
                text = str(people)
                if not self.is_allowed(line_number, cell_number):
                    text = "xx"
                elif self.get_people_at(line_number, cell_number) is None:
                    text = "nn"
                res += "[" + text + "]"
            res += "\n"
        return res

    def __init__(self):
        self.placement = []
        self.score = 0
        self.create_seats()

    '''
        Initialise le placement
    '''
    def create_seats(self):
        for line_number, cells in enumerate(Plan.grid):
            self.placement.append([])
            for cell_number, cellValue in enumerate(cells):
                self.placement[line_number].append(None)

    def get_people_at(self, line, cell):
        return self.placement[line][cell]

    def set_people_at(self, line, cell, name):
        self.placement[line][cell] = name
        self.calculate_score()

    def gen_random(self):
        # AUTRE APPROCHE
        # on prend les personnes une par une et on les place au hasard
        list_seats = []
        for line_number, cells in enumerate(Plan.grid):
            for cell_number, cellValue in enumerate(cells):
                if self.is_allowed(line_number, cell_number):
                    list_seats.append([line_number, cell_number])

        full = False
        for group in Plan.groups:
            if full:
                break
            for groupNb in range(group.nb):
                # toutes les places sont prises
                if len(list_seats) == 0:
                    full = True
                    break
                else:
                    tries = 0
                    while True:
                        # on prend une place au hasard pour cette personne
                        index_selected = random.randint(0, len(list_seats) - 1)
                        seat_selected = list_seats[index_selected]
                        line_number = seat_selected[0]
                        cell_number = seat_selected[1]

                        add_allowed = True
                        if group.constraint is not None:
                            if not group.constraint.is_allowed(line_number, cell_number):
                                add_allowed = False

                        # TODO: trouver mieux que 100
                        if tries > 100:
                            add_allowed = True
                        if add_allowed:
                            self.set_people_at(line_number, cell_number, group.name)
                            del list_seats[index_selected]
                            break
                        else:
                            tries += 1


        # people = []
        # for group in Plan.groups:
        #     for groupNb in range(group.nb):
        #         people.append(group)

        # for line_number, cells in enumerate(Plan.grid):
        #     self.placement.append([])
        #     for cell_number, cellValue in enumerate(cells):
        #         if len(people) == 0:
        #             ' on a fait le tour des gens, on met None à toutes les places '
        #             self.placement[line_number].append(None)
        #         elif not self.is_allowed(line_number, cell_number):
        #             ' siège non autorisé '
        #             self.placement[line_number].append(None)
        #         else:
        #             ' on prend une personne au hasard et on la place '
        #             add_allowed = True
        #             tries = 0
        #             while True:
        #                 index_selected = random.randint(0, len(people) - 1)
        #                 people_selected = people[index_selected]
        #                 if people_selected.constraint is not None:
        #                     if people_selected.constraint.is_allowed(line_number, cell_number):
        #                         add_allowed = True
        #                     else:
        #                         add_allowed = False
        #                         tries += 1
        #
        #                 if tries > 100:
        #                     print("tries > 100")
        #                 # TODO: Trouver mieux que '100' pour le max d'essais
        #                 if add_allowed or tries > 100:
        #                     # On ajoute la personne à cette place si :
        #                         # - Pas de contrainte
        #                         # - La place match avec la contraine
        #                         # - On a testé 100 fois et tjr pas trouvé, tant pis pour la contrainte
        #                     self.placement[line_number].append(people_selected.name)
        #                     del people[index_selected]
        #                     break  # Simule un do while

        self.calculate_score()

    def calculate_score(self):
        """
        quand à côté : +10
        quand un au dessus ou en dessous : +2 """

        score = 0
        for line_number, cells in enumerate(self.placement):
            for cell_number, people in enumerate(cells):
                if people is not None:
                    # people besides
                    if ((cell_number > 0 and self.get_people_at(line_number, cell_number - 1) == people) or
                            (cell_number < len(self.placement[line_number]) - 1 and
                             self.get_people_at(line_number, cell_number + 1) == people)):
                        score += 10
                    # people top or bottom
                    if ((line_number > 0 and self.get_people_at(line_number - 1, cell_number) == people) or
                            (line_number < len(self.placement) - 1 and self.get_people_at(line_number + 1, cell_number) == people)):
                        score += 2
        self.score = score
        return score

    def create_from_parents(self, mother, father):
        # cut at a line
        middle = len(mother.placement) / 2
        if middle % 2 != 0:
            # odd : we randomly choose the middle
            middle = round(middle)
            # on met "-" car arrondi au supérieur en cas d'impair donc + de chance d'être haut
            middle -= random.randint(0, 1)
        middle = int(middle)

        self.placement = mother.placement[0:middle] + father.placement[middle:]
        self.calculate_score()

    def is_allowed(self, line, cell):
        return self.grid[line][cell] == 1

    def is_available(self, line, cell):
        return self.is_allowed(line, cell) and self.get_people_at(line, cell) is None

    def correct_placement(self):
        # Corriger le plan
        lost_people = []
        to_much_people = []
        # 1. On cherche les personnes disparues (par mutation)
        for group in Plan.groups:
            nb_to_find = group.nb
            actual_nb = 0
            for line_number, cells in enumerate(self.placement):
                for cell_number, people in enumerate(cells):
                    if people == group.name:
                        actual_nb += 1

            if actual_nb > nb_to_find:
                for i in range(nb_to_find, actual_nb):
                    to_much_people.append(group.name)
            elif nb_to_find > actual_nb:
                for i in range(actual_nb, nb_to_find):
                    lost_people.append(group.name)

        # 2. On reprend le plan, on corrige les places interdites en enlevant les personnes dessus
        for line_number, cells in enumerate(self.placement):
            for cell_number, people in enumerate(cells):
                # Si quelqu'un est sur une place interdite, on le del et on l'ajoute aux disparus
                if not self.is_allowed(line_number, cell_number) and people is not None:
                    lost_people.append(people)
                    self.set_people_at(line_number, cell_number, None)

        # Ensuite on enlève les personnes en trop
        for line_number, cells in enumerate(self.placement):
            for cell_number, people in enumerate(cells):
                if people in to_much_people:
                    index_to_much = to_much_people.index(people)
                    del to_much_people[index_to_much]
                    self.set_people_at(line_number, cell_number, None)

                ' Si (après corrections) cette place est dispo, on y met une personne perdue'
                if len(lost_people) > 0 and self.is_available(line_number, cell_number):
                    self.set_people_at(line_number, cell_number, lost_people[0])
                    del lost_people[0]

        self.calculate_score()
