from ingestor.clients.jobtracker import extract_company, extract_position

def test_bmo_application_extraction():
    message = {
        "subject": "We’ve Received Your Application for Software Engineer - R250030923",
        "body": """
        Hello Kevin,

        Thank you for your interest in BMO.

        We have received your application for Software Engineer - R250030923
        and are currently reviewing your skills and experiences to determine
        if there’s a good fit.

        If there’s a match, a member of our recruitment team will connect with you.
        """,
    }
    company = extract_company(message)
    position = extract_position(message, company=company)
    assert company == "Bmo"
    assert position == "Software Engineer"