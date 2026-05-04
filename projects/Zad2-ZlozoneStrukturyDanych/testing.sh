#!/bin/bash

sizesList=()
for ((i=10; i<=16; i++)); do
    sizesList+=($((2**i)))
done
iterationsCount=4
resultsFile="wynikiBenchmarkow.csv"

echo "N,Tree,Create_t,MinMax_t,InOrder_t,Rebalance_t" > $resultsFile
echo "Benchmark się zaczyna się!"

for nodesCount in "${sizesList[@]}"; do
    treeData=$(seq 1 $nodesCount | tr '\n' ' ')
    
    for treeType in "bst" "avl"; do
        echo "Benchmarkowanie $treeType przy N = $nodesCount..."
        sumCreate=0; sumMinMax=0; sumInOrder=0; sumRebalance=0
        
        for i in $(seq 1 $iterationsCount); do
            pythonOutput=$(python3 main.py --tree $treeType --benchmark <<EOF
$nodesCount
$treeData
FindMinMax
Print
Rebalance
Exit
EOF
)
            
            timeCreate=$(echo "$pythonOutput" | grep "Create benchmarked" | awk '{print $4}' | tr -d '(')
            timeMinMax=$(echo "$pythonOutput" | grep "FindMinMax benchmarked" | awk '{print $4}' | tr -d '(')
            timeInOrder=$(echo "$pythonOutput" | grep "In-order benchmarked" | awk '{print $4}' | tr -d '(')
            timeRebalance=$(echo "$pythonOutput" | grep "Rebalance benchmarked" | awk '{print $4}' | tr -d '(')
            
            timeRebalance=${timeRebalance:-0}

            sumCreate=$(echo "$sumCreate + $timeCreate" | bc -l)
            sumMinMax=$(echo "$sumMinMax + $timeMinMax" | bc -l)
            sumInOrder=$(echo "$sumInOrder + $timeInOrder" | bc -l)
            sumRebalance=$(echo "$sumRebalance + $timeRebalance" | bc -l)
        done
        
        avgCreate=$(echo "scale=6; $sumCreate / $iterationsCount" | bc -l)
        avgMinMax=$(echo "scale=6; $sumMinMax / $iterationsCount" | bc -l)
        avgInOrder=$(echo "scale=6; $sumInOrder / $iterationsCount" | bc -l)
        avgRebalance=$(echo "scale=6; $sumRebalance / $iterationsCount" | bc -l)

        echo "$nodesCount,$treeType,$avgCreate,$avgMinMax,$avgInOrder,$avgRebalance" >> $resultsFile
    done
done

echo "Koniec. Wyniki zapisano w $resultsFile."