User Logins module
==============

Gathers unique login ids that have accessed the client computer
The module keeps historical IDs so data is not lost when login data is reset with OS upgrades, or other processes that would reset the `last` data.

Database:
* user - varchar(255) - user name associated with event



Module inspired from user_sessions by @tuxudo, script by @clburlison and @pudquick (frogor)
