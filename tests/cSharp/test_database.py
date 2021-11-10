from . import client
from app import create_app, db
from app.cSharp.models import *
from app.cSharp.views import *
import pytest


@pytest.fixture
def new_challenge():
    db.session.query(CSharpChallengeModel).delete()
    challenge = CSharpChallengeModel(code="./tests/cSharp/test-files/Example1.cs",
                                     tests_code="./tests/cSharp/test-files/Example1Test.cs",
                                     repair_objective="testing the db",
                                     complexity=5,
                                     best_score=0)
    db.session.add(challenge)
    db.session.commit()
    return challenge


@pytest.fixture
def expected_challenge(new_challenge):
    return new_challenge.__repr__()


@pytest.fixture
def expected_challenge_w_f_contents(new_challenge):
    challenge = new_challenge.__repr__()
    challenge['code'] = 'using System;\n\npublic class Example1 {\n    public static string example1() {\n        return "I\'m not a test";\n    }\n    public static void Main(string[] args) {\n        Console.WriteLine (example1());\n    }\n}\n'
    challenge['tests_code'] = 'using NUnit.Framework;\n\n[TestFixture]\npublic class Example1Test {\n    [Test]\n    public void test1() {\n        string result = Example1.example1();\n        Assert.AreEqual("I\'m a test", result);\t\n    }\n}\n'
    return challenge


def test_get_challenge_from_db_without_files_contents(client, expected_challenge):
    # Test get_challenge_db method with show_files_content=False
    ch_id = expected_challenge['id']
    challenge_from_get = get_challenge_db(ch_id)
    assert challenge_from_get == expected_challenge


def test_get_challenge_from_db_with_files_contents(client, expected_challenge_w_f_contents):
    ch_id = expected_challenge_w_f_contents['id']
    challenge_from_get = get_challenge_db(ch_id, show_files_content=True)
    assert challenge_from_get == expected_challenge_w_f_contents
