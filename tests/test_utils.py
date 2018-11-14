"""Unit tests the utils module of Matchlight SDK."""
import matchlight


def test_blind_name():
    """Verify test cases for blind_name."""
    test_cases = [
        (None, '*****'),
        ('', '*****'),
        ('a', 'a****'),
        ('foobar', 'f****'),
        ('terbiumlabs', 't****'),
    ]
    for case, expected in test_cases:
        assert matchlight.utils.blind_name(case) == expected


def test_blind_email():
    """Verify test cases for blind_email."""
    test_cases = [
        (None, '*****'),
        ('', '*****'),
        ('a@terbiumlabs.com', 'a****@terbiumlabs.com'),
        ('ab@terbiumlabs.com', 'a****@terbiumlabs.com'),
        ('abc@terbiumlabs.com', 'a****@terbiumlabs.com'),
        ('abcd@terbiumlabs.com', 'ab****@terbiumlabs.com'),
        ('abcde@terbiumlabs.com', 'ab****@terbiumlabs.com'),
        ('abcdef@terbiumlabs.com', 'abc****@terbiumlabs.com'),
        ('abcdefg@terbiumlabs.com', 'abc****@terbiumlabs.com'),
        ('abcdefgh@terbiumlabs.com', 'abc****@terbiumlabs.com'),
    ]
    for case, expected in test_cases:
        assert matchlight.utils.blind_email(case) == expected
