from app import create_app, db
import pytest
from app.auth.usermodel import User


@pytest.fixture(scope='module')
def client():
    # Arrange
    app = create_app('testing')
    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        # Establish an application context
        with app.app_context():
            db.create_all()
            # Tests will be executed on the test_client object
            yield test_client

            # Cleanup
            # FIXME: Pablo: I guess this is not needed for an in-memory DB?
            # db.drop_all()


def test_add_user(client):
    user = User(username='admin', password='pass')
    db.session.add(user)
    db.session.commit()

    assert len(User.query.filter_by(username='admin').all()) != 0
