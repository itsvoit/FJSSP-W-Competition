make build-prod

help(){
    echo "========================================================="
    echo ""
    echo "  Usage: $0 <RUNS> <PATH>"
    echo "    RUNS    how to many times to execute the instance"
    echo "    PATH    path to the application executable file"
    echo ""
    echo "========================================================="
}

RUNS=$1
EXEC=$2

if [ -z "$EXEC" ] || [ -z "$RUNS" ]; then
    help
    exit 1
fi

# No --append to truc the output experiments file
python -m prepare_experiments u -e "$EXEC" -o out/logs/uncertainty-factor10 -n "$RUNS" -i instances/fjssp-w -a -f 10.0 --nohup
# --append to create one big experiments files
python -m prepare_experiments u -e "$EXEC" -o out/logs/uncertainty-factor5 -n "$RUNS" -i instances/fjssp-w -a -f 5.0 --nohup
python -m prepare_experiments u -e "$EXEC" -o out/logs/uncertainty-factor2 -n "$RUNS" -i instances/fjssp-w -a -f 2.0 --nohup