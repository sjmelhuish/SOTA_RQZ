# SOTA_RQZ
Python code to obtain alerts and spots with RQZ restrictions using the SOTA public API

The SOTA public API is documented [here](https://api2.sota.org.uk/docs/index.html)

Running this script will print spots and alerts for summits within the W4V and W7V SOTA
associations for which restrictions are flagged (in respect of Green Bank or Sugar Grove).
Spots only within the last hour are checked.

Example output (from test alerts / spots):

```
List of restricted spots in last hour:
W4V/LX-002 "4386" at 2022-11-26T11:58:59.407, frequencies "1296"

List of restricted alerts:
W4V/LX-001 "Paddy Knob" at 2022-11-26T11:58:16, frequencies "1296-fm"`
```
Example output when there are no alerts / spots with restrictions:
```
List of restricted spots in last hour:
None

List of restricted alerts:
None
```
