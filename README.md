# License Checker Tool
The License Checker is a webbased tool to support researchers to choose an appropriate open source license for their research software or code. It gives an overview over common open source licenses and offers to upload code and dependency files to check for exisiting licenses and suggest compatible licenses. 

## How to install and use

Clone and run the code
```
git clone --recursive https://github.com/izus-fokus/LicenseChecker.git
cd LicenseChecker
docker compose up
```
Open in a browser http://localhost:5173/

## Acknowledgement
The development of the License Checker tool was funded by the German Research Foundation (DFG) - project number 425911815


## Quadlets configuration steps

    podman network create resus

    systemctl --user start engine.service

    systemctl --user start backend.service

    systemctl --user start frontend.service

## Bash command init startup

    podman network create resus && systemctl --user daemon-reload && systemctl --user start engine.service && systemctl --user start backend.service && systemctl --user start frontend.service

## Bash command startup

    systemctl --user daemon-reload && systemctl --user start engine.service && systemctl --user start backend.service && systemctl --user start frontend.service

## Bash command shutdown

    systemctl --user daemon-reload && systemctl --user stop engine.service && systemctl --user stop backend.service && systemctl --user stop frontend.service && systemctl --user stop postgres-container.service && systemctl --user stop fossology.service

## Frontend logging setup

    /var/log/licensechecker/nginx  ←→  /var/log/nginx  (inside container)

  The :z label tells SELinux to relabel the host directory so the container can write to it. Before restarting the
  service, create the host directory:

  sudo mkdir -p /var/log/licensechecker/nginx

  Then reload the quadlet and restart the service:

  sudo systemctl daemon-reload
  sudo systemctl restart frontend.service

  After that, navigation.log (the route log from today's change) and the standard Nginx access.log / error.log will
  all be accessible at /var/log/licensechecker/nginx/ on the host.