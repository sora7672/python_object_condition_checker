# Check conditions on you object attribute!
Well you can easy do it with comparsion, but when you want to have customization for these checks,
e.g. you want to save that to a database or file this is what you want!

## Why should i use this?
Its simple, lightweight and makes it easy to save your condition/conditionlist as json or dict.

## How to setup
Take the object_condition_checker.py and place it inside your project.
Import the `ConditionList` and place it as attribute in one of your classes.
Then create a methode on that object like this:
```python
def __init(self):
  # your stuff
  self.condtion_list: ConditionList = ConditionList()


def check_conditions(self):
  if self.condition_list.is_true():
    # do your stuff

```

To grab the json of a conditionlist/condition use:
`self.condition_list.json()`

Do with it what you can imagine ;)
I used it for user created conditions, which i save to the database and load on programstart.
Based on that i labeled some data for analysis.

HAPPY CODING!
