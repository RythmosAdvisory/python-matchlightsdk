import csv
import json

from matchlight import Matchlight


def load_fingerprints():
    '''Load data generated by fingerprint-documents.py'''
    output = []
    with open('fingerprints.json', 'r') as jsonfile:
        return json.load(jsonfile)


def main():
    '''Upload a previsouly fingerprinted set of documents.'''
    fingerprint_data = load_fingerprints()

    # Tip: You can generate your Matchlight API keys through the
    # Matchlight web interface
    # https://python-matchlightsdk.readthedocs.io/en/latest/guide.html?highlight=keys#authentication
    ml = Matchlight(
        access_key='your-matchlight-api-access-key',
        secret_key='your-matchlight-api-secret-key'
    )
    # Tip: Make sure you have already created a project
    # https://python-matchlightsdk.readthedocs.io/en/latest/guide.html#create-a-new-project
    project = ml.projects.get('your-project-upload-token')

    total_records = len(fingerprint_data)
    for counter, document_fingerprint in enumerate(fingerprint_data):
        print(
            f'Uploading {document_fingerprint["name"]} '
            f'({counter} of {total_records})'
        )
        ml.records.add_document_from_fingerprints(
            project, document_fingerprint
        )


if __name__ == '__main__':
    main()
