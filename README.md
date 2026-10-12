# Programming with Python (202044504) - Assignment 1

Python 3.10+ solutions for Q1-Q10.

## Student

**Name:** Yatharth Mehta
**Enrollment No.:** 12402080601160
**Assignment:** 1

## Repository structure

- `12402080601160_Assignment1_Q1.py` - lists, tuples, dictionaries, sorting
- `12402080601160_Assignment1_Q2.py` - regular expressions + Aho-Corasick
- `12402080601160_Assignment1_Q3.py` - recursive parsing + memoization + cycle detection
- `12402080601160_Assignment1_Q4.py` - CSV validation + exception-safe processing
- `12402080601160_Assignment1_Q5.py` - OOP + custom exceptions + batch rollback
- `12402080601160_Assignment1_Q6.py` - graph + heap + topological sorting
- `12402080601160_Assignment1_Q7.py` - interactive calculator + custom exceptions
- `12402080601160_Assignment1_Q8.py` - pickle + inverted index + ZIP
- `12402080601160_Assignment1_Q9.py` - priority scheduling + simulated workers
- `12402080601160_Assignment1_Q10.py` - Tkinter GUI + JSON + CSV

## Run

All programs use only Python standard-library modules.

Examples:

```bash
python 12402080601160_Assignment1_Q1.py < q1_input.txt
python 12402080601160_Assignment1_Q2.py < q2_input.txt
python 12402080601160_Assignment1_Q3.py < q3_input.txt
python 12402080601160_Assignment1_Q4.py transactions.csv
python 12402080601160_Assignment1_Q5.py < q5_input.txt
python 12402080601160_Assignment1_Q6.py < q6_input.txt
python 12402080601160_Assignment1_Q7.py
python 12402080601160_Assignment1_Q8.py < q8_build.txt
python 12402080601160_Assignment1_Q9.py < q9_input.txt
python 12402080601160_Assignment1_Q10.py
```

## Notes

- Q4 creates `credit.csv`, `debit.csv` and `error.csv`.
- Q8 BUILD creates a pickle index and a ZIP archive containing the index and logs.
- Q9 uses deterministic simulated time. The assignment does not define a global resource-capacity limit, so the `resources` field is retained as job metadata while worker availability controls execution.
- Q10 persists records in `assignment_data.json` and can export all records to CSV.

Before submission, replace/add your own test evidence and verify every program against your faculty's exact interpretation.

## Important assignment note

The Q1 document's sample says semester 3 should be `2205 2203`, but the supplied
marks give Chaitra (2203) an average of 90.33 and Esha (2205) an average of
89.67. The stated rule says to prefer the higher average, so the implementation
follows the written rule and produces `2203 2205`. If your faculty expects the
printed sample literally, confirm which interpretation they want before submission.

The Q5 implementation keeps a failed batch open until `BATCH_END`; all mutations
after the first failure are ignored and the complete batch is rolled back.

## Self-created test examples

For additional testing, use ordinary Indian names and identifiers such as:
- Aditi, Rohan, Mehul, Priya, Neha and Arjun
- Accounts such as SBI001, HDFC102 and AXIS205
- Modules such as `billing`, `orders`, `reports` and `login`

These are supplementary test values; the official assignment samples remain unchanged.
