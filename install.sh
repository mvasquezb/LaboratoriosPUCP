#!/usr/bin/env sh

echo "Running database setup"
./db_setup.sh
echo "Done."

echo "Running app setup"
./app_setup.sh
echo "Done."
