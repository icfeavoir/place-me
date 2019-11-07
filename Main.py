from Chief import *
from dotenv import load_dotenv
import os
import csv

load_dotenv()

TEST = int(os.getenv("TEST")) == 1

if __name__ == '__main__':

    chief = Chief()
    if not TEST:
        chief.start(False)

    def test_with_val(ch, writer, nb_gen, nb_p, prob_m, nb_r):
        ch.NB_GENERATION = nb_gen
        ch.NB_PLANS = nb_p
        ch.PROB_MUTATIONS = prob_m
        ch.NB_REPRODUCTION = nb_r
        ch.NB_REPRODUCTION = round(ch.NB_PLANS * ch.NB_REPRODUCTION)
        data_to_insert = [ch.NB_GENERATION, ch.NB_PLANS, ch.PROB_MUTATIONS, ch.NB_REPRODUCTION]

        best_score = -1
        best_at = 0
        total = 0
        for i in range(TRIES_NUMBER):
            plan, time_ga = ch.start(TEST)
            total += 1
            if plan.score > best_score:
                best_score = plan.score
                best_at = total
            data_to_insert.append(plan.score)
            data_to_insert.append(str(time_ga).replace(".", ","))

        data_to_insert.append(best_at)
        data_to_insert.append(total)
        writer.writerow(data_to_insert)

    if TEST:
        TRIES_NUMBER = 5
        with open('results.csv', mode='w') as results_file:
            results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            columns = [
                "NB_GENERATION",
                "NB_PLANS",
                "PROB_MUTATIONS",
                "NB_REPRODUCTION",
            ]
            for i in range(TRIES_NUMBER):
                columns.append("S" + str(i + 1))
                columns.append("T" + str(i + 1))
            columns.append("BEST_AT")
            columns.append("TOTAL_TRIES")
            results_writer.writerow(columns)

            # +mutation
            test_with_val(chief, results_writer, 1000, 100, 0.1, 0.5)
            test_with_val(chief, results_writer, 1000, 200, 0.1, 0.5)
            test_with_val(chief, results_writer, 500, 100, 0.4, 0.6)
            test_with_val(chief, results_writer, 500, 100, 0.6, 0.6)
            test_with_val(chief, results_writer, 500, 100, 0.6, 0.8)

        print("DONE")
