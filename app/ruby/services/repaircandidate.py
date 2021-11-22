from nltk import edit_distance
from .rubycode import RubyCode, RubyTestsCode


class RepairCandidate:
    """Provide handling of the given candidate solution."""

    def __init__(self, challenge, repair_code, path):
        """Initialize candidate.

        Parameters:
            challenge (RubyChallenge): get the Challenge that the user wants to solve,
            repair_code (RubyCode): get the candidate solution from the user,
            path (str):  set where the files are stored.
        """
        self.challenge = challenge
        self.repair_code = RubyCode()
        self.repair_code.set_code(path, self.challenge.code.get_file_name(), repair_code)
        self.path = path

    def save_candidate(self):
        """Save the candidate solution.

        Attributes:
            repair_code (RubyCode): the candidate solution to save.
        """
        self.repair_code.save()

    def compiles(self):
        """Compile the given candidate solution.

        Attributes:
            repair_code (RubyCode): the candidate solution to compile.
        """
        return self.repair_code.compiles()

    def tests_ok(self):
        """Check that the candidate solution satisfies the challenge tests.

        Attributes:
            test_suite (RubyTestCode): challenge tests saved in the same path as the candidate solution.

        Returns:
            bool: confirmation that the tests do not fail with the candidate solution.

        """
        test_suite = RubyTestsCode(full_name=self.challenge.tests_code.copy(self.path))
        return not test_suite.run_fails()

    def compute_score(self):
        """get the score obtained from the candidate solution.
        
        Returns:
            int: the edit distance the of the challenge and the candidate solution.
        """
        return edit_distance(self.repair_code.get_content(), self.challenge.code.get_content())

    def get_content(self, username, attempts, score):
        """Obtain a dict with information about the challenge,
        the user and the number of times they proposed a solution.

        Parameters:
            username (str): the name of the user,
            attempts (int): the number of attempts to repair the challenge,
            score (int): the score obtained from the candidate solution.

        Attributes:
            challenge (RubyChallenge): the challenge to repair.

        Returns:
            dict: repair information.
        """
        return {'repair': {
            'challenge': self.challenge.get_content(exclude=['id', 'code', 'tests_code', 'complexity']),
            'player': {'username': username},
            'attempts': str(attempts),
            'score': score}
        }
