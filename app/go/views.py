from . import go
from .go_controller import Controller

controller = Controller()

@go.route('api/v1/go-challenges/<int:id>/repair', methods=['POST'])
def repair_challenge_go(id):
    return controller.post_repair(id)

@go.route('/api/v1/go-challenges', methods=['GET'])
def get_challenges():
    return controller.get_all_challenges()

@go.route('/api/v1/go-challenges/<id>', methods=['GET'])
def get_challenge(id):
    return controller.get_challenge_by_id(id)

@go.route('/api/v1/go-challenges/<id>', methods=['PUT'])
def update_a_go_challenge(id):
    return controller.update_a_go_challenge(id)
    
@go.route('/api/v1/go-challenges', methods=['POST'])
def create_go_challenge():
    return controller.post_challenge()