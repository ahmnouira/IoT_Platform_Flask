#! /bin/sh
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    printf  "%s\n"  "Deloy command failed, retrying in 5 secs..."
done

exec gunicorn -b 0.0.0.0:5000 --access-logfile - --error-logfile - main:App
