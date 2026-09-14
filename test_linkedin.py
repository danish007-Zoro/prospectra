from src.linkedin import linkedin_url_matches_name


def test_linkedin_url_matches_correct_name():
    url = "https://www.linkedin.com/in/abhinavasthana/"
    assert linkedin_url_matches_name(url, "Abhinav Asthana")


def test_linkedin_url_rejects_wrong_person():
    url = "https://www.linkedin.com/in/abhinavasthana/"
    assert not linkedin_url_matches_name(url, "Abhijit Kane")


def test_linkedin_url_accepts_slug_with_suffix():
    url = "https://www.linkedin.com/in/ankit-sobti-98b0ab19/"
    assert linkedin_url_matches_name(url, "Ankit Sobti")