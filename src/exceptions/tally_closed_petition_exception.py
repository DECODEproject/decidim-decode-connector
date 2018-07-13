class TallyClosedPetitionException(Exception):
    def __str__(self):
        return "Can't tally a closed petition"
