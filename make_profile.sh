# profiles the example program
# the only argument is what to
# append to the name of the
# output file pout
python -m cProfile -s time example.py >| pout${1}
