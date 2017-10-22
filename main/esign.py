def sign():
    doc = {
        "documents": [
            {
                "documentBase64": "FILE1_BASE64",
                "documentId": "1",
                "fileExtension": "pdf",
                "name": "NDA.pdf"
            }
        ],
        "emailSubject": "Please sign the NDA",
        "recipients": {
            "signers": [
                {
                    "email": "dwibedy@usc.edu",
                    "name": "Chris",
                    "recipientId": "1",
                    "routingOrder": "1",
                    "tabs": {
                        "dateSignedTabs": [
                            {
                                "anchorString": "signer1date",
                                "anchorYOffset": "-6",
                                "fontSize": "Size12",
                                "name": "Date Signed",
                                "recipientId": "1",
                                "tabLabel": "date_signed"
                            },
                        ],
                        "fullNameTabs": [
                            {
                                "anchorString": "signer1name",
                                "anchorYOffset": "-6",
                                "fontSize": "Size12",
                                "name": "Full Name",
                                "recipientId": "1",
                                "tabLabel": "Full Name"
                            }
                        ],
                        "signHereTabs": [
                            {
                                "anchorString": "signer1sig",
                                "anchorUnits": "mms",
                                "anchorXOffset": "0",
                                "anchorYOffset": "0",
                                "name": "Please sign here",
                                "optional": "false",
                                "recipientId": "1",
                                "scaleValue": 1,
                                "tabLabel": "signer1sig"
                            }
                        ]
                    }
                }
            ]
        },
        "status": "sent"
    }
    doc['recipients']['signers'][0]['email'] = 'manish.dwibedy@gmail.com'
    doc['recipients']['signers'][0]['name'] = 'Dummy name'

    import json
    with open('send_signing_request_by_email.json', 'w') as outfile:
        json.dump(doc, outfile)

    import subprocess
    # subprocess.check_output(['ls','-l']) #all that is technically needed...
    print subprocess.check_output(["sed -e \"s/FILE1_BASE64/$(sed 's:/:\\/:g' main/Mutual_NDA.pdf.base64) main/send_signing_request_by_email.json > main/payload.json"])
