import random, time

random.seed(42)

def generate_assignments(num_assignment):
    """Generate exam assignments with random raw scores (0–100).
    """
    return [{"id": i, 
             "raw_score": random.randint(0, 100)} for i in range(num_assignment)]


def grade_assignment(assignment):
    """Grade assignment.
    Return grade 1-3 based on raw_score.
    """
    # Simulate marking time (varies per paper)
    time.sleep(0.05 * (1 + assignment["id"] * 0.2))

    # Raw Score from assignment (raw_score 0-100)
    raw_score = assignment["raw_score"]

    # Convert raw score to grade (1-3)
    if raw_score >= 70:
        return 1
    elif raw_score >= 60:
        return 2
    else:
        return 3
