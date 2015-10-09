#matrixWidth=3
#matrixHeight=3
#matrixUpperBound=10
debug=1
test_mat_mul:*.cpp
	g++ -O3 mat_mul.cpp mat_mul_golden_algo.cpp mat_mul_unfolded_algo_transformed.cpp -o mat_mul.out -g 
run_test:
	./mat_mul.out 0 $(matrixWidth) $(matrixHeight) $(matrixUpperBound)

run_test_debug:
	./mat_mul.out 1 $(matrixWidth) $(matrixHeight) $(matrixUpperBound)


clean:*.out
	rm *.out
