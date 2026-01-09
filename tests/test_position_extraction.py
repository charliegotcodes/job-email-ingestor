from ingestor.clients.jobtracker import position_check_body

def test_linkedin_application_position_extraction():
    body = """
    your application was sent to aaron consulting inc.
    junior software developer
    aaron consulting inc.
    greater toronto area, canada
    """

    company = "Aaron Consulting Inc"

    position = position_check_body(body, company)

    assert position == "Junior Software Developer"
