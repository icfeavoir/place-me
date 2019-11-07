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

    def test_with_val(ch, writer, name, nb_gen, nb_p, prob_m, nb_r):
        ch.NB_GENERATION = nb_gen
        ch.NB_PLANS = nb_p
        ch.PROB_MUTATIONS = prob_m
        ch.NB_REPRODUCTION = nb_r
        ch.NB_REPRODUCTION = round(ch.NB_PLANS * ch.NB_REPRODUCTION)
        writer.writerow([name])

        data_to_insert = [ch.NB_GENERATION, ch.NB_PLANS, ch.PROB_MUTATIONS, ch.NB_REPRODUCTION]

        for i in range(TRIES_NUMBER):
            plan, time_ga, best_at, total = ch.start(TEST)
            data_to_insert.append(plan.score)
            data_to_insert.append(str(time_ga).replace(".", ","))
            data_to_insert.append(str(best_at) + " /" + str(total))
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

            results_writer.writerow(columns)

            test_with_val(chief, results_writer, "Changement nb plans", 500, 100, 0.05, 0.5)
            test_with_val(chief, results_writer, "Changement nb plans", 500, 200, 0.05, 0.5)
            test_with_val(chief, results_writer, "Changement nb plans", 500, 300, 0.05, 0.5)
            test_with_val(chief, results_writer, "Changement nb plans", 500, 500, 0.05, 0.5)
            test_with_val(chief, results_writer, "Changement nb plans", 500, 800, 0.05, 0.5)

            test_with_val(chief, results_writer, "Changement léger generations", 1000, 200, 0.05, 0.5)
            test_with_val(chief, results_writer, "Changement léger generations", 2000, 200, 0.05, 0.5)

            test_with_val(chief, results_writer, "variation prob_mutation", 500, 100, 0.02, 0.5)
            test_with_val(chief, results_writer, "variation prob_mutation", 500, 100, 0.05, 0.5)
            test_with_val(chief, results_writer, "variation prob_mutation", 500, 100, 0.1, 0.5)
            test_with_val(chief, results_writer, "variation prob_mutation", 500, 100, 0.15, 0.5)
            test_with_val(chief, results_writer, "variation prob_mutation", 500, 100, 0.2, 0.5)
            test_with_val(chief, results_writer, "variation prob_mutation", 500, 100, 0.25, 0.5)

            test_with_val(chief, results_writer, "variation reproduction", 500, 100, 0.05, 0.1)
            test_with_val(chief, results_writer, "variation reproduction", 500, 100, 0.05, 0.2)
            test_with_val(chief, results_writer, "variation reproduction", 500, 100, 0.05, 0.3)
            test_with_val(chief, results_writer, "variation reproduction", 500, 100, 0.05, 0.4)
            test_with_val(chief, results_writer, "variation reproduction", 500, 100, 0.05, 0.5)
            test_with_val(chief, results_writer, "variation reproduction", 500, 100, 0.05, 0.6)
            test_with_val(chief, results_writer, "variation reproduction", 500, 100, 0.05, 0.7)
            test_with_val(chief, results_writer, "variation reproduction", 500, 100, 0.05, 0.8)
            test_with_val(chief, results_writer, "variation reproduction", 500, 100, 0.05, 0.9)

            test_with_val(chief, results_writer, "variation mut + rep sur generations fortes", 2000, 100, 0.1, 0.2)
            test_with_val(chief, results_writer, "variation mut + rep sur generations fortes", 2000, 100, 0.2, 0.2)
            test_with_val(chief, results_writer, "variation mut + rep sur generations fortes", 2000, 100, 0.2, 0.5)
            test_with_val(chief, results_writer, "variation mut + rep sur generations fortes", 2000, 100, 0.2, 0.7)
            test_with_val(chief, results_writer, "variation mut + rep sur generations fortes", 2000, 100, 0.2, 0.8)

            test_with_val(chief, results_writer, "generations extremes", 5000, 100, 0.05, 0.5)
            test_with_val(chief, results_writer, "generations extremes", 10000, 100, 0.05, 0.6)

        print("DONE")
