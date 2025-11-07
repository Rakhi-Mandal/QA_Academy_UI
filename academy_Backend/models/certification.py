from database.connection import get_db_connection, close_db_connection
from database.queries import (GET_ALL_CERTIFICATIONS, GET_CERTIFICATION_BY_ID, CREATE_CERTIFICATION,UPDATE_CERTIFICATION, DELETE_CERTIFICATION, CHECK_CERTIFICATION_EXISTS,CHECK_CERTIFICATION_HAS_RECORDS, GET_CERTIFICATIONS_WITH_STATS)
from typing import List, Dict, Optional, Tuple
import datetime


def get_all_certifications() -> List[Dict]:
    connection = get_db_connection()
    if not connection:
        return []

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(GET_ALL_CERTIFICATIONS)
        certifications = cursor.fetchall()

        for c in certifications:
            if isinstance(c.get("Deadline_Date"), (datetime.date, datetime.datetime)):
                c["Deadline_Date"] = c["Deadline_Date"].isoformat()

        return certifications
    finally:
        cursor.close()
        close_db_connection(connection)


def get_certification_by_id(certification_id: str) -> Optional[Dict]:
    connection = get_db_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(GET_CERTIFICATION_BY_ID, (certification_id,))
        certification = cursor.fetchone()

        if certification and isinstance(certification.get("Deadline_Date"), (datetime.date, datetime.datetime)):
            certification["Deadline_Date"] = certification["Deadline_Date"].isoformat()

        return certification
    finally:
        cursor.close()
        close_db_connection(connection)


def create_certification(certification_id: str, name: str, deadline_date: Optional[str], link: Optional[str]) -> bool:
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        cursor.execute(CREATE_CERTIFICATION, (certification_id, name, deadline_date, link))
        connection.commit()
        return True
    finally:
        cursor.close()
        close_db_connection(connection)
