# vim4-fanctl

I didn't like the VIM4's limited fan speed controls, so I built a daemon to fine tune its behavior.

Only tested on my specific system. Use at your own risk.

## Installation

1. `chmod +x fanctl.py`
2. Put `fanctl.py` in `/usr/local/bin/`
3. Put `fanctl.service` in `/etc/systemd/system/`
4. `systemctl enable fanctl`
5. `systemctl start fanctl`
