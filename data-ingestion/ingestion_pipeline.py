import logging
import sys

from config import DBConfig

LOGGER = logging.getLogger(__name__)


def _split_and_validate(row):
    gre_score, toefl_score, ug_univ_rating, sop_score, lor_score, gpa, research, admit = row.split(',')

    gre_score, toefl_score, ug_univ_rating, sop_score, lor_score, gpa, research, admit = \
        int(gre_score), int(toefl_score), int(ug_univ_rating), float(sop_score), float(lor_score), float(gpa), int(research), int(admit)

    assert 340 >= gre_score >= 170
    assert 120 >= toefl_score >= 80
    assert 5 >= ug_univ_rating >= 1
    assert 5.0 >= sop_score >= 0.0
    assert 5.0 >= lor_score >= 0.0
    assert 5.0 >= gpa >= 0.0
    assert research == 0 or research == 1
    assert admit == 0 or admit == 1

    return gre_score, toefl_score, ug_univ_rating, sop_score, lor_score, gpa, research, admit


def _ingest_row(connection, columns):
    insert_query = '''
        INSERT INTO grad_admission(gre_score, toefl_score, ug_univ_rating, sop_score, lor_score, gpa, research, admit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''
    with connection.cursor() as cur:
        cur.execute(insert_query, *columns)
    LOGGER.info('ingested one row')


def ingest():
    input_data = sys.stdin.readlines()
    connection = DBConfig().get_connection()
    for row in input_data:
        row = row.rstrip()
        try:
            columns = _split_and_validate(row)
            _ingest_row(connection, columns)
        except Exception as e:
            LOGGER.warning('Error in row: {}, skipping...'.format(row), exec_info=sys.exc_info())

    LOGGER.info('all standard input records consumed...')
    sys.exit()


if __name__ == '__main__':
    ingest()
