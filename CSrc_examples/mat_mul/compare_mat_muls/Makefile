#matrixWidth=3
#matrixHeight=3
#matrixUpperBound=10
test_mat_mul:*.cpp
	g++ --std=c++11 -O3 compare_mat_muls.cpp ../mat_mul_golden_algo.cpp ../mat_mul_unfolded_algo.cpp -o mat_mul.out -g -I../ -I../../../inc/BookKeeping/ -I../../../inc/OperatorHeaders/ -I../../../inc/MotionEstimationHeaders/
run_test:
	./mat_mul.out $(debug) $(matrixWidth) $(matrixHeight) $(matrixUpperBound) $(randomSeed)

clean:*.out
	rm ../*.out ../*unfolded_algo
