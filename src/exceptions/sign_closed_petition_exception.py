class SignClosedPetitionException(Exception):
    def __str__(self):
        return "We are sorry, this petition has now closed."
