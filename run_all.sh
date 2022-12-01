for i in {1..25};
do
    python3 run_solution.py --day "$i" --task 01 --retry 1
    python3 run_solution.py --day "$i" --task 02 --retry 1
done
