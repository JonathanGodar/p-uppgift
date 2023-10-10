import datetime as dt
from typing import List

# This function takes a prompt and a a list of "transformations"
# each transformation will be applied in order
# The input to each transformation is the output of the previous one - The first transformation gets the user input as a str
# If a transformation raises an error the user will be presented with the error message and prompted to try again.
# This new input will then pass by all of the transformations.
# This cycle is continued until the user gives an input that passes all transformations
def get_from_user_with_transformations(prompt: str, transformations):
	user_input = input(prompt + ": ")
	try:
		for transformation in transformations:
				user_input = transformation(user_input) 
	except Exception as e:
		return get_from_user_with_transformations(str(e)+ ", försök igen", transformations) 
		
	return user_input


def get_int_from_user(prompt: str, transformations=[]):
	return get_from_user_with_transformations(prompt, [to_int_transformation] + transformations) 

def get_positive_int_from_user(prompt: str, transformations=[]):
	return get_int_from_user(prompt, [is_positive_validation] + transformations)

def get_float_from_user(prompt: str, transformations=[]):
	return get_from_user_with_transformations(prompt, [to_float_transformation] + transformations)

def get_positive_float_from_user(prompt: str, transformations = []):
	return get_float_from_user(prompt, [is_positive_validation] + transformations)

def get_date_from_user(prompt, transformations = []) -> dt.date:
	return get_from_user_with_transformations(prompt, [to_date_transformation] + transformations) # type: ignore

def get_alternative_from_user(prompt, alternatives, transformations=[]):
	return get_from_user_with_transformations(prompt, [create_is_one_of_validation(alternatives)] + transformations)


# Validations(transformations that do not modify the input)
def is_positive_validation(input):
	if input <= 0:
		raise Exception("Det där talet är inte positivt")
	return input

def create_is_one_of_validation(alternatives):
	def is_one_of_validation(input):
		if not input in alternatives: 
			alternatives_str = ', '.join(list(map(lambda alt: str(alt), alternatives)))
			raise Exception(f'Det där är inte ett giltigt alternativ. [Välj bland: {alternatives_str}]')
		return input
	return is_one_of_validation 
	
# Transformations
def to_int_transformation(input) -> int:
	try:
		return int(input)
	except:
		raise Exception("Det där är inte ett heltal")

def to_float_transformation(input) -> float:
	try:
		return float(input)
	except:
		raise Exception("Det där är inte ett tal")

def to_date_transformation(input):
	DATE_FORMAT = "%Y-%m-%d"
	DATE_FORMAT_HUMAN_READABLE = "ÅÅÅÅ-MM-DD"
	try:
		return dt.datetime.strptime(input, DATE_FORMAT).date()
	except:
		raise Exception(f'Det där är inte ett datum i rätt format ({DATE_FORMAT_HUMAN_READABLE})')