#!/usr/bin/env bash

beanie migrate \
  -p migrations \
  -uri "mongodb+srv://kaustubhkadam147_db_user:OTxSsWVdfJmtzH7l@test-jwt.e16rsrg.mongodb.net/?appName=test-jwt" \
  -db auth_db