'''
This module contains example functions demonstrating differeny ways of
filtering and pulling down Matchlight alerts data.
'''

import records
from matchlight import Matchlight


def setup_example_database(db):
    # Create a new example database everytime with some fake data.
    # Tip: In this example we just store the alert number for simplicity
    # but in your application you should store all the alert object
    # metadata.
    # Reference: https://python-matchlightsdk.readthedocs.io/en/latest/api.html#alert
    db.query('DROP TABLE IF EXISTS alerts')
    db.query(
        'CREATE TABLE alerts (id int PRIMARY KEY, number int)'
    )
    db.query(
        'INSERT INTO alerts '
        'VALUES      ("39de2145a1d66330b9d443a84c90d34f", 1)'
    )
    return db


def get_last_alert(db):
    return db.query(
        'SELECT Max(alerts.number) AS max_alert_number FROM alerts'
    )[0]


def save_new_alert(db, new_alert):
    db.query(
        f'INSERT INTO alerts (id, number) '
        f'VALUES     ("{new_alert.id}", "{new_alert.number}")'
    )


def get_number_of_local_alerts(db):
    return db.query('SELECT Count(*) as count from alerts')[0].count


def get_and_store_alerts():
    # Create a database connection and set up a local alert database.
    # db = records.Database('sqlite:///matchlight-alerts-example.db')
    db = records.Database('sqlite:///:memory:')
    setup_example_database(db)
    print(
        f'Number of alerts in databasse is {get_number_of_local_alerts(db)}'
    )

    # Create a Matchliht API connection
    # Tip: You can generate your Matchlight API keys through the
    # Matchlight web interface
    # https://python-matchlightsdk.readthedocs.io/en/latest/guide.html?highlight=keys#authentication
    # ml = Matchlight(
    #     access_key='your-matchlight-api-access-key',
    #     secret_key='your-matchlight-api-secret-key'
    # )
    ml = Matchlight(
        access_key='your-matchlight-api-access-key',
        secret_key='your-matchlight-api-secret-key'
    )

    # Grab a Matchlight project with multiple alerts.
    project = ml.projects.get('your-project-upload-token')

    # Uncomment to reset all you Matchlight data every time.
    # set_all_alerts_as_unseen(ml, project)

    last_alert = get_last_alert(db)
    print(f'Latest alert is number {last_alert.max_alert_number}')

    keep_going = True
    while keep_going:
        alert_query = ml.alerts.filter(project=project, limit=1, seen=False)
        if len(alert_query) == 0:
            print('No unseen alerts left')
            break
        else:
            new_alert = alert_query[0]
        print(f'New Alert found with Alert Number {new_alert.number}')
        if new_alert.number > last_alert.max_alert_number:
            save_new_alert(db, new_alert)
            ml.alerts.edit(new_alert.id, seen=True)
            print(f'Alert Number {new_alert.number} set to "seen"')
        else:
            keep_going = False
            print('No new alerts remain')
    print(
        f'Number of alerts in databasse is {get_number_of_local_alerts(db)}'
    )


def set_all_alerts_as_unseen(ml, project):
    '''
    This is utility function that resets the last 50 alerts in a
    project to unseen. This had no application in production but is a
    development utility to reset test data.
    '''
    print('Resetting Alerts')
    last_fifty_alerts = ml.alerts.filter(project=project, limit=50)
    print(f'Found {len(last_fifty_alerts)} alerts')
    for alert in last_fifty_alerts:
        print(f'Setting alert number {alert.number} as seen.')
        ml.alerts.edit(alert.id, seen=False)


if __name__ == '__main__':
    get_and_store_alerts()
