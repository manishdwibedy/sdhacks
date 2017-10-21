
POST https://demo.docusign.net/restApi/v2/accounts/{accountId}/envelopes

{
  "status": "sent",
  "emailSubject": "Request a signature via email example",
  "documents": [
    {
      "documentId": "1",
      "name": "contract.pdf",
      "documentBase64": "[base64 encoded file bytes...]"
    }
  ],
  "recipients": {
    "signers": [
      {
        "name": "[SIGNER NAME]",
        "email": "[SIGNER EMAIL ADDRESS]",
        "recipientId": "1",
        "tabs": {
          "signHereTabs": [
            {
              "xPosition": "25",
              "yPosition": "50",
              "documentId": "1",
              "pageNumber": "1"
            }
          ]
        }
      }
    ]
  }
}
