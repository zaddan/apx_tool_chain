#include <iostream>
using namespace std;
int main() {
  cout << "hello there";
  int arrSize = 9; 
  int array[arrSize];
  for (int i =0; i< arrSize; i++) {
      array[i] = i; //MultiplicationOp
  }
  for (int i =0; i< arrSize; i++) {
      cout << array[i]<<endl; //AdditionOp
  }



}
