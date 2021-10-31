
class PythonChallengeDAO:

  def get_all_challenges():
    return PythonChallengeModel.query.all()

  def get_challenge(id):
    return PythonChallengeModel.query.filter_by(id = id).first()

  def create_challenge(code_path, test_path, repair_objective, complexity):
    new_challenge = PythonChallengeModel(code=new_code_path,
        tests_code=new_tests_path,
        repair_objective=challenge_data['repair_objective'],
        complexity=challenge_data['complexity'],
        best_score=0)

    db.session.add(new_challenge)
    db.session.commit()

  def update_challenge(id, new_data):
    db.session.query(PythonChallengeModel).filter_by(id=id).update(dict(new_data))
    db.session.commit()