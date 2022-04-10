
import math
from corpus import Corpus
from results.results import Results
from results.evaluations import Evaluations
from results.score import Score


class EvaluateResults:
    WEIGHT_DECREASE = 0.90
    MAXIMUM_SCORE = 2
    FIRST_X_COUNTED_TO_COVERAGE = 50

    evaluations: Evaluations
    scores: list[Score] = []
    average_final_score: float
    average_relevance_score: float
    average_coverage_score: float
    average_ndcg_score: float

    def evaluate(self, results_file_path: str, evaluations_path: str, corpus: Corpus):
        # Load results
        results = Results()
        results.load_results_csv(results_file_path)

        # Modify result ids to be evaluation compatible
        results.remove_section_identifiers()

        # Load evaluations from the file
        self.evaluations = Evaluations(evaluations_path)

        # Remove unnecessary evaluations
        self.evaluations.clean_non_essential_evaluations_using_corpus(corpus)

        # Calculate scores
        self.calculate_scores(results)

        # Sort list of scores
        self.scores.sort(key=lambda score: score.query_id)

        # Calculate averages
        self.calculate_scores_average()

        # Print results
        print(self)

    def calculate_scores(self, results: Results):
        # Evaluate correctness of the results using premade evaluations
        results_grouped_by_id = results.group_by_topic_number()
        for query_id in results_grouped_by_id.keys():
            (relevance_score, scored_with_maximum_grade_amount) = self.calculate_relevance_score(
                query_id, results_grouped_by_id)

            coverage_score = self.calculate_coverage_score(
                query_id, scored_with_maximum_grade_amount)

            # Calculate nDCG score
            idcg_score = self.calculate_idcg(query_id)
            ndcg_score = self.calculate_ndcg(
                query_id, results_grouped_by_id, idcg_score)

            # Calculate final score by weighting relevance and coverage scores
            final_score = relevance_score * 0.30 + coverage_score * 0.15 + ndcg_score * 0.55

            # Save score to list of scores
            score = Score(query_id, final_score,
                          relevance_score, coverage_score, ndcg_score)
            self.scores.append(score)

    def calculate_relevance_score(self, query_id: int, results_grouped_by_id: dict[list[Results]]) -> tuple[float, int]:
        # Calculate scores based on the evaluations.
        # This step makes 80 percent of the score.
        # Full score is given, if the entry is evaluated with score self.MAXIMUM_SCORE
        # and no score is given, if evaluation is 0.
        # First entries are weighted more. Weight of the next entries is
        # decreased by 5% every time. If result is not evaluated,
        # it is not counted towards target.
        raw_relevance_score = 0
        scored_entries_amount = 0
        scored_with_maximum_grade = {}
        for result in results_grouped_by_id.get(query_id):
            # Do not consider entries that are not evaluated
            if result.document_id not in self.evaluations.entries.get(query_id):
                continue

            # Add to score based on the grade and weight
            raw_relevance_score += self.evaluations.entries[query_id][result.document_id] * \
                self.WEIGHT_DECREASE ** scored_entries_amount

            # Increase the amount of scored entries
            scored_entries_amount += 1

            # If score was maximum, add it to the maximum grade amount
            # Note only first x amount of entries are considered
            # Related to next score category
            if self.evaluations.entries[query_id][result.document_id] == self.MAXIMUM_SCORE and \
                    scored_entries_amount < self.FIRST_X_COUNTED_TO_COVERAGE:
                scored_with_maximum_grade[result.document_id] = True

        # Calculate theoretical maximum score based on the scored entries amount
        theoretical_maximum_score = 0
        for amount in range(scored_entries_amount):
            theoretical_maximum_score += self.MAXIMUM_SCORE * self.WEIGHT_DECREASE ** amount

        # Calculate relevance percentage
        if theoretical_maximum_score != 0:
            relevance_score = raw_relevance_score / theoretical_maximum_score
        else:
            relevance_score = 0

        scored_with_maximum_grade_amount = len(scored_with_maximum_grade)
        return (relevance_score, scored_with_maximum_grade_amount)

    def calculate_coverage_score(self, query_id: int, scored_with_maximum_grade_amount: dict[str]) -> float:
        # Calculate coverage score.
        # Score is 20% of the total score.
        # Coverage score signifies amount of best scores that
        # were caught (or left caught).
        # Calculate how many points there are available at maximum for the query
        maximum_coverage_amount = 0
        for evaluation in self.evaluations.entries.get(query_id).values():
            if evaluation == self.MAXIMUM_SCORE:
                maximum_coverage_amount += 1

        # Calculate final coverage score
        # Score will be capped to one since in theory there can be more entries scored with
        # maximum grade than there are entries in the evaluation, because new corpus is
        # divided into more parts
        if maximum_coverage_amount != 0:
            coverage_score = scored_with_maximum_grade_amount / maximum_coverage_amount
        else:
            coverage_score = 1

        return coverage_score

    def calculate_idcg(self, query_id: int) -> float:
        # Order evaluations
        ordered_evaluations = sorted(self.evaluations.get_query_evaluations(
            query_id), reverse=True)

        # Calculate IDCG value
        idcg_score = 0
        for index, ordered_evaluation in enumerate(ordered_evaluations):
            idcg_score += ordered_evaluation / math.log2(index + 2)

        return idcg_score

    def calculate_ndcg(self, query_id: int, results_grouped_by_id: dict[list[Results]], idcg_score: float):
        # Dictionary of allready evaluated ids.
        # Evaluate every id only once.
        allready_evaluated = {}

        # Calculate DCG value
        dcg_score = 0
        for index, result in enumerate(results_grouped_by_id.get(query_id)):
            # Skip if allready evaluated id
            if result.document_id in allready_evaluated:
                continue
            else:
                allready_evaluated[result.document_id] = True

            # Get relevance score
            relevance = self.evaluations.entries[query_id].get(
                result.document_id)

            # Do not consider entries that are not evaluated
            if not relevance:
                continue

            # Calculate new DCG score
            dcg_score += relevance / math.log2(index + 2)

        # Calculate nDCG score
        ndcg_score = dcg_score / idcg_score

        return ndcg_score

    def calculate_scores_average(self):
        final_score_sum = 0
        relevance_score_sum = 0
        coverage_score_sum = 0
        ndcg_score_sum = 0
        for score in self.scores:
            final_score_sum += score.score
            relevance_score_sum += score.relevance_score
            coverage_score_sum += score.coverage_score
            ndcg_score_sum += score.ndcg_score

        scores_amount = len(self.scores)

        self.average_final_score = final_score_sum / scores_amount
        self.average_relevance_score = relevance_score_sum / scores_amount
        self.average_coverage_score = coverage_score_sum / scores_amount
        self.average_ndcg_score = ndcg_score_sum / scores_amount

    def __repr__(self) -> str:
        output = ""
        output += "Query id | Score | Relevance score | Coverage score | nDCG\n"
        for score in self.scores:
            final_score = round(score.score, 2)
            relevance_score = round(score.relevance_score, 2)
            coverage_score = round(score.coverage_score, 2)
            ndcg_score = round(score.ndcg_score, 2)
            output += f"{score.query_id} {final_score} {relevance_score} {coverage_score} {ndcg_score}\n"

        # Rounded averages
        average_final_score = round(self.average_final_score, 2)
        average_relevance_score = round(self.average_relevance_score, 2)
        average_coverage_score = round(self.average_coverage_score, 2)
        average_ndcg_score = round(self.average_ndcg_score, 2)
        output += f"Average {average_final_score} {average_relevance_score} {average_coverage_score} {average_ndcg_score}"

        return output

    def save_results_to_file(self, file_path: str):
        # Open results file for writing
        try:
            results_file = open(file_path, "w")
        except OSError as error:
            print(error)
            print(
                "Couldn't open evaluation results file for writing, is the file path correct?")
            exit(1)

        # Write results
        results_file.write(self.__repr__())
        results_file.close()

        print(f'Evaluation results saved to the "{file_path}"')
