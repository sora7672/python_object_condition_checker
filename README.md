# Check conditions on your object attributes!
Well you can easy do it with comparsion, but when you want to have customization for these checks,
e.g. you want to save that to a database or file this is what you want!

## Why should i use this?
Its simple, lightweight and makes it easy to save your condition/conditionlist as json or dict.
For further usage in database or files.
This enables you to save on changes or program close and read them in on program start.

## How to setup
Take the object_condition_checker.py and place it inside your project.
Import the `ConditionList` and place it as attribute in one of your classes.
Then create a methode on that object like this:
```python
class MyTest:
  def __init(self):
    # your attributes
    self.condtion_list: ConditionList = ConditionList(...)  # Obviously need to create here some conditions
  
  
  def check_conditions(self):
    if self.condition_list.is_true():
      # do your stuff

```

To grab the json of a conditionlist/condition use:
`self.condition_list.json()`

If you want to check protected or private attributes, make sure to create a property named as the check you want to run.
Like this:
```py
class MyClass:
  def __init__(self):
    self._my_protected = 1234
    self.__my_private = "Bananas"

  @property
  def my_protected(self):
    return self._my_protected

  @porperty
  def my_private(self):
    return self.__my_private


```

Do with it what you can imagine ;)
I used it for user created conditions, which i save to the database and load on programstart.
Based on that i labeled some data for analysis.

HAPPY CODING!
