from app.java.models_java import Challenge_java
from . import java


class DAO_java_challenge():

      def all_challenges_java():
        return  Challenge_java.query.all()
    