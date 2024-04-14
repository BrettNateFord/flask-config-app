# flask-config-app
Flask app in development. Provides a UI to configure various project variables from the web

Features:
Configure parsing rules: allow the creation, alteration, or deletion of JSON parsing rules specific to parsing NMEA0183 and NMEA2000 data, changes are saved to the parsing_rules.json file
Configure Power BI credentials: allow the editing of information relevant to user's Power BI REST API credentials
Sample Data viewer: This feature is antiquated, will be changed to show the data stream in progress
Parsed Data viewer: This feature will show the data after its alterations, essentially right before sendoff
