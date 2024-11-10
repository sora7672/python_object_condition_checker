from datetime import datetime, date, time
import json


class ObjectCondition:
    """
     Represents a single condition to evaluate an attribute of an object
     based on a specified comparison operator and value.

     Attributes:
         _accepted_comp_operators_strings: Operators valid for string comparisons.
         _accepted_comp_operators_numbers: Operators valid for numeric comparisons.
         _accepted_comp_operators_lists: Operators valid for list-based comparisons.
         _accepted_value_types: Supported data types for the condition's attribute value.
     """
    _accepted_comp_operators_strings = ("==", "!=", "in", "not in")
    _accepted_comp_operators_numbers = ("<", ">", "<=", ">=", "==", "!=")
    _accepted_comp_operators_lists = ("in", "not in")
    _accepted_comp_operators = tuple(set(_accepted_comp_operators_strings +
                                         _accepted_comp_operators_numbers +
                                         _accepted_comp_operators_lists))
    _accepted_value_types = ("str", "int", "float", "date", "datetime", "time")

    def __init__(self, attribute_name: str, comp_operator: str,
                 attribute_value: str | int | float | date | datetime | time, value_type: str = "str"):
        """
        Initializes an ObjectCondition instance with a specified attribute, comparison operator, value, and value type.

        :param attribute_name: Name of the attribute to be evaluated on the object.
        :param comp_operator: Comparison operator, must be one of the accepted types.
        :param attribute_value: The value to compare against.
        :param value_type: The type of the attribute, default is 'str'.
        """

        if value_type not in self._accepted_value_types:
            raise ValueError(f"Value type {value_type} is not accepted. Accepted types: {self._accepted_value_types}")
        if comp_operator not in self._accepted_comp_operators:
            raise ValueError("Comp operators not supported")

        self._attribute_name: str = attribute_name
        self._comp_operator: str = comp_operator

        match value_type:
            case "str":
                if self._comp_operator not in self._accepted_comp_operators_strings:
                    raise ValueError(f"Comp operator {self._comp_operator} not supported for strings")
                self._attribute_value = str(attribute_value)

            case "int":
                if self._comp_operator not in self._accepted_comp_operators_numbers:
                    raise ValueError(f"Comp operator {self._comp_operator} not supported for numbers")
                self._attribute_value = int(attribute_value)

            case "float":
                if self._comp_operator not in self._accepted_comp_operators_numbers:
                    raise ValueError(f"Comp operator {self._comp_operator} not supported for numbers")
                self._attribute_value = float(attribute_value)

            case "date":
                if self._comp_operator not in self._accepted_comp_operators_numbers:
                    raise ValueError(f"Comp operator {self._comp_operator} not supported for numbers")
                self._attribute_value = self.parse_datetime(attribute_value).date()

            case "time":
                if self._comp_operator not in self._accepted_comp_operators_numbers:
                    raise ValueError(f"Comp operator {self._comp_operator} not supported for numbers")
                self._attribute_value = self.parse_datetime(attribute_value).time()

            case "datetime":
                if self._comp_operator not in self._accepted_comp_operators_numbers:
                    raise ValueError(f"Comp operator {self._comp_operator} not supported for numbers")
                self._attribute_value = self.parse_datetime(attribute_value)

            case _:
                raise ValueError(f"Invalid value type {value_type}")

        self._value_type = value_type

    def is_true(self, obj: object) -> bool:
        """
        Evaluates the condition against an attribute of the given object.

        :param obj: The object containing the attribute to be checked.
        :return: Boolean indicating if the condition holds true for the given object.
        """
        if not hasattr(obj, self._attribute_name):
            raise AttributeError(f"Condition evaluation error.\nObject ({obj}) has no attribute {self._attribute_name}")

        test_value = getattr(obj, self._attribute_name)
        if not isinstance(test_value, type(self._attribute_value)):
            raise TypeError(f"Condition evaluation error.\nObject ({obj}) attribute type {type(test_value)} "
                            f"is not type {type(self._attribute_value)}")

        match self._comp_operator:
            case "in":
                return test_value in self._accepted_comp_operators_lists

            case "not in":
                return test_value not in self._accepted_comp_operators_lists

            case "<":
                return test_value < self._attribute_value

            case ">":
                return test_value > self._attribute_value

            case "<=":
                return test_value <= self._attribute_value

            case ">=":
                return test_value >= self._attribute_value

            case "==":
                return test_value == self._attribute_value

            case "!=":
                return test_value != self._attribute_value

            case _:
                raise Exception(f"Unknown comparison operator {self._comp_operator}")

    def dict(self) -> dict:
        """
        Serializes the condition to a dictionary.

        :return: A dictionary with the condition's parameters.
        """
        data = {
            "attribute_name": self._attribute_name,
            "comp_operator": self._comp_operator,
            "attribute_value": str(self._attribute_value),
            "value_type": self._value_type
        }
        return data

    def json(self) -> str:
        """
        Serializes the condition to a JSON string.

        :return: JSON string representation of the condition.
        """
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, data: str| dict) -> 'ObjectCondition':
        """
        Creates an ObjectCondition instance from a JSON string or dictionary.

        :param data: A JSON string or dictionary with condition parameters.
        :return: ObjectCondition instance initialized with the given data.
        """
        if isinstance(data, str):
            data = json.loads(data)
        elif not isinstance(data, dict):
            raise ValueError("Input must be a JSON string or a dictionary.")

        return cls(
            attribute_name=data["attribute_name"],
            comp_operator=data["comp_operator"],
            attribute_value=data["attribute_value"],
            value_type=data["value_type"]
        )

    @staticmethod
    def parse_datetime(value: str) -> datetime:
        """
        Parses a date/time from string or timestamp.
        :param value: string with timestamp or date.
        :return: datetime object representing the given value.
        """
        if value.replace('.', '', 1).isdigit():
            timestamp = float(value)
            return datetime.fromtimestamp(timestamp)
        elif "-" in value and ("T" in value or len(value) == 10):
            if len(value) == 10:
                return datetime.fromisoformat(value + "T00:00:00")
            else:
                return datetime.fromisoformat(value)
        else:
            raise ValueError("Input is not a recognized Unix timestamp or ISO datetime format.")

    def __str__(self) -> str:
        return f"Condition on {self._attribute_name} {self._comp_operator} {self._attribute_value} ({self._value_type})"


class ConditionList:
    """
    Represents a collection of ObjectCondition and ConditionList objects
    with a specified logical operator.

    Attributes:
      _accepted_boolean_operators: Operators valid for combining conditions (and, or).
    """
    _accepted_boolean_operators = ("and", "or")

    def __init__(self, *conditions: ObjectCondition | 'ConditionList', operator: str = "and"):
        """
        Initializes a ConditionList with specified conditions and logical operator.

        :param conditions: Conditions to be evaluated as a list of ObjectCondition or ConditionList instances.
        :param operator: Logical operator to apply across conditions, either 'and' or 'or'.
        """
        self.conditions = []
        if operator not in self._accepted_boolean_operators:
            raise ValueError("Operator not supported")
        self.operator = operator.lower()

        for condition in conditions:
            if isinstance(condition, ObjectCondition) or isinstance(condition, ConditionList):
                self.conditions.append(condition)
            else:
                raise ValueError(f"Invalid condition type {type(condition)}")

    def is_true(self, obj: object) -> bool:
        """
        Evaluates all conditions in the list using the specified logical operator.

        :param obj: Object to check conditions against.
        :return: Boolean indicating the result of all combined conditions.
        """
        result_list = []
        for condition in self.conditions:
            result = condition.is_true(obj)
            result_list.append(result)

        final_result = result_list[0][0]
        for result in result_list[1:]:
            if self.operator == "and":
                final_result = final_result and result
            elif self.operator == "or":
                final_result = final_result or result
            else:
                raise ValueError(f"Unknown operator: {self.operator}")

        return final_result

    def dict(self) -> dict:
        """
        Serializes the ConditionList to a dictionary.

        :return: A dictionary with 'operator' and 'conditions' keys.
        """
        return {
            "operator": self.operator,
            "conditions": [condition.dict() for condition in self.conditions]
        }

    def json(self) -> str:
        """
        Serializes the ConditionList to a JSON string.

        :return: JSON string representing the ConditionList.
        """
        return json.dumps(self.dict())

    @classmethod
    def from_json(cls, data: str | dict) -> 'ConditionList':
        """
        Creates a ConditionList instance from a JSON string or dictionary.

        :param data: A JSON string or dictionary with 'operator' and 'conditions'.
        :return: ConditionList instance populated with the specified conditions and operator.
        """
        if isinstance(data, str):
            data = json.loads(data)
        elif not isinstance(data, dict):
            raise ValueError("Input must be a JSON string or a dictionary.")

        operator = data.get("operator", "and")
        conditions = [
            ObjectCondition.from_json(cond) if isinstance(cond, dict) and "attribute_name" in cond else cls.from_json(
                cond)
            for cond in data.get("conditions", [])
        ]

        return cls(*conditions, operator=operator)

    def __str__(self) -> str:
        conditions_str = f" {self.operator.upper()} ".join(str(cond) for cond in self.conditions)
        return f"ConditionList({conditions_str})"

