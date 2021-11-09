import os
import pytest
from app import create_app, db
from . import client
#from app.cSharp.models import CSharp_Challenge

def test_post_challenge(client):
    #Arrange
    url = 'cSharp/c-sharp-challenges/'
    '''
    expected_response = {
        "best_score": 0, 
        "code": "using System;\n\npublic class Example1 {\n    public static string example1() {\n        return \"I'm not a test\";\n    }\n    public static void Main(string[] args) {\n        Console.WriteLine (example1());\n    }\n}\n", 
        "complexity": 1, 
        "id": 1, 
        "repair_objective": "Make all tests pass.", 
        "tests_code": "using NUnit.Framework;\n\n[TestFixture]\npublic class Example1Test {\n    [Test]\n    public void test1() {\n        string result = Example1.example1();\n        Assert.AreEqual(\"I'm a test\", result);\t\n    }\n}\n"
        
    }
    '''
   
    #create challenge
    code_file = open('tests/cSharp/test-files/Example1.cs', 'rb')
    code_test_file = open('tests/cSharp/test-files/Example1Test.cs', 'rb')
    challenge = {
        'source_code_file': code_file,
        'test_suite_file': code_test_file,
        'challenge': '{ \
            "challenge": { \
                "source_code_file_name" : "code_challenge", \
                "test_suite_file_name" : "code_test", \
                "repair_objective" : "repair", \
                "complexity" : "3" \
            } \
        }'
    }
    ret_post = client.post(url, data=challenge)
    #ret_post_json = ret_post.json['challenge']
    #del ret_post_json['id'] 
    
    #assert
    assert ret_post.status_code == 200
    #assert ret_post_json == expected_response
    
    
#def test_post_repair(client):
    #Arrange
    #path_test='/test-files/MedianRepair.cs'
    #file_repair = {'source_code_file': open(path_test, 'r')}
    #Act


    #Assert
    #pass 