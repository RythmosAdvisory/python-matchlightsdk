import records
from matchlight import Matchlight

from local_alert_utilities import (
    get_last_saved_alert,
    get_number_of_local_alerts,
    save_new_alert,
    setup_example_database,
)


def get_and_store_alerts():
    # Create a database connection and set up a local alert database.
    # db = records.Database('sqlite:///matchlight-alerts-example.db')
    db = records.Database('sqlite:///:memory:')
    setup_example_database(db)
    print(
        f'Number of alerts in database is {get_number_of_local_alerts(db)}'
    )

    # Create a Matchliht API connection
    # Tip: You can generate your Matchlight API keys through the
    # Matchlight web interface
    # https://python-matchlightsdk.readthedocs.io/en/latest/guide.html?highlight=keys#authentication
    ml = Matchlight(
        access_key='78f42f60b1d44dda97e2ca3ee4bf88bb',
        secret_key='574fe283b64744bdb2331ac67fcfcbcc'
    )

    # Grab a Matchlight project with multiple alerts.
    project = ml.projects.get('b4c3253f-2c71-420e-a0ae-3f92daea697a')

    # Find the last saved alert in our database. We will work backwards
    # through the new alerts until we get to this value.
    last_saved_alert = get_last_saved_alert(db)
    print(f'Latest alert is number {last_saved_alert.max_alert_number}')

    keep_going = True
    last_alert_query_parameter = None
    while keep_going:
        print(f'Last Alert Query Parameter is {last_alert_query_parameter}')
        alert_query = ml.alerts.filter(
            project=project, limit=1, last_alert=last_alert_query_parameter
        )
        if len(alert_query) == 0:
            print('No alerts left')
            break
        else:
            new_alert = alert_query[0]
        print(f'New Alert found with Alert Number {new_alert.number}')
        if new_alert.number > last_saved_alert.max_alert_number:
            save_new_alert(db, new_alert)
            last_alert_query_parameter = new_alert.number
        else:
            keep_going = False
            print('No new alerts remain')
    print(
        f'Number of alerts in databasse is {get_number_of_local_alerts(db)}'
    )


if __name__ == '__main__':
    get_and_store_alerts()
