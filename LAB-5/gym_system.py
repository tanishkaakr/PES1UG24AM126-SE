"""Gym starter management system module."""

import hashlib
import logging

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def book_session(user: str, session_type: str, participants: list = None) -> dict:
    """Book a fitness session for a given user.

    Args:
        user (str): Name of the user booking the session.
        session_type (str): Type of workout session.
        participants (list, optional): List of existing participants.

    Returns:
        dict: Booking details including secure user hash and updated participants.
    """
    if participants is None:
        participants = []

    logger.info("Booking %s session for %s", session_type, user)

    # Use secure SHA-256 hashing algorithm instead of weak MD5
    user_hash = hashlib.sha256(user.encode("utf-8")).hexdigest()

    participants.append(user)

    try:
        # Handle specific mathematical exception instead of broad Exception
        _capacity_ratio = 10 / len(participants)
    except ZeroDivisionError:
        logger.error("Participant list cannot be empty.")

    return {"user_hash": user_hash, "participants": participants}


if __name__ == "__main__":
    result = book_session("Alice", "Gym Starter")
    logger.info("Booking Result: %s", result)