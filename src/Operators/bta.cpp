#include <iostream>
#include <complex>
#include <vector>
#include "bta.h"
#include "globals.h"
#include "fp_helpers.h"
using namespace std;

bta::bta(size_t Nt, size_t Nia, size_t msb, size_t lsb, bool table_gen) {
	this->Nt = Nt;
	this->Nia = Nia;
	this->msb = msb;
	this->lsb = lsb;

	if (table_gen) tbl_gen();

}

bta::~bta(void) {}

size_t bta::get_ianum_bits(void) {
	return Nia;
}

float bta::calc(const float &number1, const int &number2) {
    #ifdef VERBOSE 
    cout<<"=============insde half float"<<endl; 
    #endif 
    float numOut = number2; 
    calc(number1, numOut);
} 

float bta::calc(const int &number1, const float &number2) {
    cout<<"=============insde other half float"<<endl; 
    float numOut = number1; 
    calc(numOut, number2);
} 



float bta::calc(const float &number1, const float &number2) {
    fpType num1;
    fpType num2;
    float apxResult; 
    fpType result; 
    fpType bigNum;
    fpType smallNum;
    int signMultiplicand; 
    getFPComponents(number1, num1); //get the fp componenets
    getFPComponents(number2, num2); //get the fp components
    num1.MantisaWithOne = (1 <<MANTISA_WIDTH) + num1.Mantisa;//injaect mantisa with Extra one
    num2.MantisaWithOne =   (1 <<MANTISA_WIDTH) + num2.Mantisa;//injaect mantisa with Extra one
     
    if (num1.Exp  < num2.Exp) { //decide on the small and big number
      bigNum = num2;
      smallNum = num1;
    }  else {
      bigNum = num1;
      smallNum = num2;
    }
    
    smallNum.MantisaWithOne = smallNum.MantisaWithOne >> (bigNum.Exp - smallNum.Exp); // align the small num
    if (bigNum.Sign == smallNum.Sign) { //same sign
        result.Mantisa = (bigNum.MantisaWithOne +  smallNum.MantisaWithOne);
        result.Exp = bigNum.Exp;
        result.Sign = bigNum.Sign;
        normalizeAdd(result);
        result.Mantisa =  (result.Mantisa >> Nia) << Nia; //truncate mantisa
        result.Mantisa =  result.Mantisa - (1<<MANTISA_WIDTH); 
        apxResult = convertFPCompToFP(result);
    }else{ //diff sign
            result.Mantisa = (bigNum.MantisaWithOne - smallNum.MantisaWithOne);
            result.Exp = bigNum.Exp;
            result.Sign = bigNum.Sign; 
            normalizeAdd(result);
            result.Mantisa =  (result.Mantisa >> Nia) << Nia; //truncate mantisa
            result.Mantisa =  result.Mantisa - (1<<MANTISA_WIDTH); 
            apxResult = convertFPCompToFP(result);
    }

    return apxResult; 
}


int bta::calc(const int &a, const int &b) {
    // inaccurate part
    #ifdef VERBOSE 
    cout<<"=============in int version"<<endl; 
    #endif  
    int weight = pow(2, Nia) - 1;
	int iap_a = weight&a;
#ifdef BT_RND
	int a_op = (iap_a >> (Nia - 1)) == 0x1 ? (a >> Nia) + 1 : (a >> Nia);
#else
	int a_op = (a >> Nia);
#endif
	int iap_b = weight&b;
#ifdef BT_RND
	int b_op = (iap_b >> (Nia - 1)) == 0x1 ? (b >> Nia) + 1 : (b >> Nia);
#else
	int b_op = (b >> Nia);
#endif

	// accurate part
	return ((a_op) + (b_op)) << Nia;
}
//
//


unsigned int bta::calc(const unsigned int &a, const unsigned int &b) {
    // inaccurate part
    #ifdef VERBOSE 
    cout<<"=============in unsigned unsigned int version"<<endl; 
    #endif  
    unsigned int weight = pow(2, Nia) - 1;
	unsigned int iap_a = weight&a;
#ifdef BT_RND
	unsigned int a_op = (iap_a >> (Nia - 1)) == 0x1 ? (a >> Nia) + 1 : (a >> Nia);
#else
	unsigned int a_op = (a >> Nia);
#endif
	unsigned int iap_b = weight&b;
#ifdef BT_RND
	unsigned int b_op = (iap_b >> (Nia - 1)) == 0x1 ? (b >> Nia) + 1 : (b >> Nia);
#else
	unsigned int b_op = (b >> Nia);
#endif

	// accurate part
	return ((a_op) + (b_op)) << Nia;
}

int bta::calc(const unsigned int &a_unsigned, const int &b) {
    // inaccurate part
    #ifdef VERBOSE 
    cout<<"=============in unsigned unsigned int version"<<endl; 
    #endif  
    int a = (int)a_unsigned; 
    int weight = pow(2, Nia) - 1;
	int iap_a = weight&(int)a;
#ifdef BT_RND
	int a_op = (iap_a >> (Nia - 1)) == 0x1 ? (a >> Nia) + 1 : (a >> Nia);
#else
	int a_op = ((int)a >> Nia);
#endif
	int iap_b = weight&b;
#ifdef BT_RND
	int b_op = (iap_b >> (Nia - 1)) == 0x1 ? (b >> Nia) + 1 : (b >> Nia);
#else
	int b_op = (b >> Nia);
#endif

	// accurate part
	return ((a_op) + (b_op)) << Nia;
}

int bta::calc(const int &a, const unsigned int &b_unsigned) {
    // inaccurate part
    #ifdef VERBOSE 
    cout<<"=============in unsigned unsigned int version"<<endl; 
    #endif  
    int b = (int)b_unsigned; 
    int weight = pow(2, Nia) - 1;
	int iap_a = weight&(int)a;
#ifdef BT_RND
	int a_op = (iap_a >> (Nia - 1)) == 0x1 ? (a >> Nia) + 1 : (a >> Nia);
#else
	int a_op = ((int)a >> Nia);
#endif
	int iap_b = weight&b;
#ifdef BT_RND
	int b_op = (iap_b >> (Nia - 1)) == 0x1 ? (b >> Nia) + 1 : (b >> Nia);
#else
	int b_op = (b >> Nia);
#endif

	// accurate part
	return ((a_op) + (b_op)) << Nia;
}




int bta::calc_ref(const int &a, const int &b) {
	// this is adder
	return a + b;
}

void bta::tbl_gen() {
	int i,j;
	int i_w, j_w;
	int calc_tmp1;
	int calc_tmp2;
	for (i=0; i<pow(2,msb-lsb+1); i++) {
		for (j=0; j<pow(2,msb-lsb+1); j++) {
			i_w = i<<lsb;
			j_w = j<<lsb;
			calc_tmp1 = calc(i_w, j_w);
			calc_tmp2 = calc_ref(i_w, j_w);

			//cout << "sglee: " << i_w << "," << j_w << ", apr: " << calc_tmp1 << ", ori: " << calc_tmp2 << endl;
			if (calc_tmp1 != calc_tmp2) {
				err_tbl.push_back(make_pair(make_pair(i_w,j_w), make_pair(make_pair(0,0),calc_tmp2-calc_tmp1)));
			}
		}
	}
}
