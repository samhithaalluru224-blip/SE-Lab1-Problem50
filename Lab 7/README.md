# SE Lab 7 – Fuzzing for Input Validation Bugs

## Files
- `daycare_fees.py` – fixed application containing `parse_enrolment`,
  `hours_average`, and `payable_fee`.
- `test_daycare_fees.py` – Hypothesis tests using the assigned repository's
  test filename.
- `test_processor.py` – same Hypothesis tests under the filename specified
  in the generic lab handout. It imports the functions from `daycare_fees.py`.
- `requirements.txt` – required Python test dependencies.

## Install dependencies
```bash
python -m pip install -r requirements.txt
```

## Run the tests
Repository filename:
```bash
python -m pytest test_daycare_fees.py -v
```

Lab-handout filename:
```bash
python -m pytest test_processor.py -v
```

Both test files exercise the three application functions with arbitrary
strings and `None` values using Hypothesis. They test that the functions
handle unexpected inputs without raising exceptions.

## Run the application
```bash
python daycare_fees.py
```


