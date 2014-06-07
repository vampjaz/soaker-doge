Doger
=====

IRC bot framework in python.

**Setup:**

- Create a file in the same folder as the code named `Config.py`, and put the following into it:

```
config = {
	"host": "IRC server hostname",
	"port": 6667,
	"user": "identname",
	"rname": "Real name",
	"password": "nickservpassword",
	"admins": {
		"foo!bar@baz": True # full hostmasks of administrators
	},
	"nicks": {
		"nick1": ["#channel1", "#channel2"],
		"nick2": ["#channel3"]
	}
}
```
    
**Running it:**

- Launch the bot with `python Main.py`
