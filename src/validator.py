from src.scraper import PageEvidence
from src.schemas import CompanyIntelligence


def validate_contact_points(
    intelligence: CompanyIntelligence,
    pages: list[PageEvidence],
) -> tuple[int, int, list[str]]:
    """
    Return contact verification statistics and unverified emails.

    Returns:
        total_contacts: Number of extracted contact emails.
        verified_contacts: Number of emails found on their source pages.
        unverified_emails: Emails that could not be verified.
    """

    total_contacts = len(intelligence.contact_points)
    verified_contacts = 0
    unverified_emails = []

    for contact in intelligence.contact_points:
        if verify_email(
            pages,
            contact.email,
            contact.source_url,
        ):
            verified_contacts += 1
        else:
            unverified_emails.append(contact.email)

    return (
        total_contacts,
        verified_contacts,
        unverified_emails,
    )


def find_source_page(
    pages: list[PageEvidence],
    source_url: str,
) -> PageEvidence | None:
    """
    Find the page corresponding to a source URL.
    """

    for page in pages:
        if page.url == source_url:
            return page

    return None


def verify_email(
    pages: list[PageEvidence],
    email: str,
    source_url: str,
) -> bool:
    """
    Check whether an extracted email appears on its claimed source page.
    """

    page = find_source_page(
        pages,
        source_url,
    )

    if page is None:
        return False

    return email.lower() in page.content.lower()


def validate_intelligence(
    intelligence: CompanyIntelligence,
    pages: list[PageEvidence],
) -> tuple[int, int, list[str], int, int, list[str]]:
    """
    Validate extracted contacts and leadership against source evidence.

    Returns:
        total_contacts,
        verified_contacts,
        unverified_emails,
        total_members,
        verified_members,
        unverified_members
    """

    (
        total_contacts,
        verified_contacts,
        unverified_emails,
    ) = validate_contact_points(
        intelligence,
        pages,
    )

    (
        total_members,
        verified_members,
        unverified_members,
    ) = validate_leadership(
        intelligence,
        pages,
    )

    return (
        total_contacts,
        verified_contacts,
        unverified_emails,
        total_members,
        verified_members,
        unverified_members,
    )


def verify_team_member(
    pages: list[PageEvidence],
    name: str,
    role: str,
    source_url: str,
) -> bool:
    """
    Check whether a person's name and role appear on their claimed source page.
    """

    page = find_source_page(
        pages,
        source_url,
    )

    if page is None:
        return False

    content = page.content.lower()

    name_found = name.lower() in content
    role_found = role.lower() in content

    return name_found and role_found

def validate_leadership(
    intelligence: CompanyIntelligence,
    pages: list[PageEvidence],
) -> tuple[int, int, list[str]]:
    """
    Return leadership verification statistics and unverified members.

    Returns:
        total_members: Number of extracted leadership members.
        verified_members: Number of members whose name and role
                          were found on their source pages.
        unverified_members: Members that could not be verified.
    """

    total_members = len(intelligence.key_leadership)
    verified_members = 0
    unverified_members = []

    for member in intelligence.key_leadership:
        if verify_team_member(
            pages,
            member.name,
            member.role,
            member.source_url,
        ):
            verified_members += 1
        else:
            unverified_members.append(member.name)

    return (
        total_members,
        verified_members,
        unverified_members,
    )