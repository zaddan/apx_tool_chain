#include <iostream>
#include <complex>
#include <vector>
#include "bta.h"
#include "globals.h"
#include "fp_helpers.h"
#include <bitset>
using namespace std;
#include <cstring>
#include <cassert>
#include <string>
#include <climits>
extern long double energy_value;

template<typename T>
void show_binrep(const T& a)
{
    const char* beg = reinterpret_cast<const char*>(&a);
    const char* end = beg + sizeof(a);
    while(beg != end)
        std::cout << std::bitset<CHAR_BIT>(*beg++) << ' ';
    std::cout << '\n';
}


bta::bta(size_t Nt, size_t Nia, size_t msb, size_t lsb, bool table_gen) {
	this->Nt = Nt;
	this->Nia = Nia;
	this->msb = msb;
	this->lsb = lsb;

	if (table_gen) tbl_gen();

}

bta::~bta(void) {}

vector <float> add_long_long_energy_vals  {1.77, 1.7653 ,1.7620 ,1.7585, 1.7495, 1.7448, 1.7369,1.7321 ,1.7278 ,1.7240 ,1.7179,1.7135,1.7092,1.7052,1.6975,1.6945};
vector <float> add_long_int_energy_vals {1.63,1.6204 , 1.6091 , 1.6080 , 1.5979 ,  1.6019, 1.5879,1.5896 ,1.5785 ,1.5811 ,1.5667,1.5715,1.5566,1.5591,1.5450, 1.5469};
vector <float> add_int_int_energy_vals{.894, .8892198 , .8846183 , .8785046 , .8740424 , .8694106 ,  .8630022 ,.8601716 ,.8548939 ,.8502534 ,.8421492, .8393752 ,.8353899 ,.8289224 ,.8231492 ,.8175684};
//--- their counters
extern vector<int> add_long_long_energy_counters;
extern vector<int> add_long_int_energy_counters;
extern vector<int> add_int_int_energy_counters;


void bta::update_energy(int n_apx_bits, string op1_type, string op2_type){
    if (op1_type == "long" && op2_type == "long") {
        energy_value += add_long_long_energy_vals[n_apx_bits]*.3; //*.3 b/c  the clock cycle was .3ns for adder vs multiplier which was 1ns
        add_long_long_energy_counters[n_apx_bits] +=1;
    }
    else if (op1_type=="int" && op2_type =="long") {
        energy_value += add_long_int_energy_vals[n_apx_bits]*.3;
        add_long_int_energy_counters[n_apx_bits] +=1;
    }
    else if (op1_type == "long" && op2_type == "int") {
        energy_value += add_long_int_energy_vals[n_apx_bits]*.3;
        add_long_int_energy_counters[n_apx_bits] +=1;
    }
    else if (op1_type == "int" && op2_type== "int") {
        energy_value += add_int_int_energy_vals[n_apx_bits]*.3;
        add_int_int_energy_counters[n_apx_bits] +=1;
    }
    else if (op1_type == "float" && op2_type == "float") {
        cout<<"^^^^^^^^^^^^^the energy value for this bta types is not defined"<<endl;
        cout<<"^^^^^^^^^^^^^"<<endl;
    }
    else {
        cout<<"the energy value for "<< op1_type <<" and "<< op2_type<<  " bta types is not defined"<<endl;
        exit(0);
    }
    //energy_valuee+= (32 - n_apx_bits) + 10;
}

size_t bta::get_ianum_bits(void) {
	return Nia;
}

//long, int version
int bta::calc(const long &a, const int &b) {
    // inaccurate part
    update_energy(Nia, "long", "int"); 

#ifdef VERBOSE 
    cout<<"=============long int version"<<endl; 
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

	return ((a_op) + (b_op)) << Nia;
}


int bta::calc(const long &a, const long &b) {
    // inaccurate part
    update_energy(Nia, "long", "long"); 

#ifdef VERBOSE 
    cout<<"=============long int version"<<endl; 
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

	return ((a_op) + (b_op)) << Nia;
}

int bta::calc(const int &a, const long &b) {
    // inaccurate part
    update_energy(Nia, "int", "long"); 
#ifdef VERBOSE 
    cout<<"=============int, long version"<<endl; 
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
	return ((a_op) + (b_op)) << Nia;
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



//float, float version

float bta::calc(const float &number1, const float &number2) {
    int a ;
    int b ;
    float z = 0; //intermediate output used in the function
    int output = 0;  //output to return
    memcpy(&a, &number1, sizeof(a));
    memcpy(&b, &number2, sizeof(b));
    /* 
    cout<<"showing a nad b"<<endl; 
    show_hex(a);
    show_hex(number1);
    show_hex(b);
    show_hex(number2);
    cout<<"add inside:"<<a+ b<<endl; 
    */ 
    int a_m; //a_mantisa
    int b_m; //b_mantisa
    int z_m; //z_mantis
   //----------------------------------------------------------------- 
    int a_e; //a_exp
    int b_e;
    int z_e;
   //----------------------------------------------------------------- 
    int a_s; //a_sign
    int b_s;
    int z_s;
   //----------------------------------------------------------------- 
   int sticky, guard, round_bit, sum;
    //unpack
#ifdef BT_RND 
    a_m = get_bits(a, 22, 0 + Nia) << 3;
    b_m = get_bits(b, 22, 0 + Nia) << 3;
#else
    a_m = get_bits(a, 22, 0 + Nia) << 3;
    b_m = get_bits(b, 22, 0 + Nia) << 3;
#endif
    a_e = get_bits(a, 30, 23) - 127;
    b_e = get_bits(b, 30, 23) - 127;
    a_s = get_bit(a, 31);
    b_s = get_bit(b, 31);

    //special_cases:
    //if a is NaN or b is NaN return NaN 
    { 
        if ((a_e == 128 && a_m != 0) || (b_e == 128 && b_m != 0)) {
            set_bit(z, 31, 1); //z[31] <= 1;
            set_bits(z, 30,23, 255); // z[30:23] <= 255;
            set_bit(z, 22,1); // z[22] <= 1;
            set_bits(z, 21, 0, 0); //z[21:0] <= 0;
            return z;
        }
        else if (a_e == 128) { //if a is inf return inf
            set_bit(z,31,a_s); //set_z[31] <= a_s;
            set_bits(z, 30, 23, 255); //z[30:23] <= 255;
            set_bits(z, 22, 0, 0); // z[22:0] <= 0;
            //if b is inf return inf
            return z; 
        }else if (b_e == 128) {
            set_bit(z, 31, b_s); //z[31] <= b_s;
            set_bits(z, 30, 23, 255); //z[30:23] <= 255;
            set_bits(z, 22, 0, 0); // z[22:0] <= 0;
            return z; 
            //if a is zero return b
        }  else if (((a_e == -127) && (a_m == 0)) && ((b_e == -127) && (b_m == 0))){
            set_bit(z, 31, a_s & b_s); //z[31] <= a_s & b_s;
            set_bits(z, 30, 23, get_bits(b_e, 7, 0) + 127); // z[30:23] <= b_e[7:0] + 127;
            set_bits(z, 22, 0 + Nia, get_bits(b_m, 26-Nia, 3)); //z[22:0] <= b_m[26:3];
            //if a is zero return b
            return z; 
        }  else if ((a_e == -127) && (a_m == 0)){
            set_bit(z, 31, b_s); //z[31] <= b_s;
            set_bits(z, 30, 23, get_bits(b_e, 7, 0) + 127); //z[30:23] <= b_e[7:0] + 127;
            set_bits(z, 22, 0+Nia, get_bits(b_m, 26-Nia, 3)); //z[22:0] <= b_m[26:3];
            return z; 
            //if b is zero return a
        }else if ((b_e == -127) && (b_m == 0)) {
            set_bit(z, 31, a_s); //z[31] <= a_s;
            set_bits(z, 30, 23, get_bits(a_e, 7, 0) + 127); //z[30:23] <= a_e[7:0] + 127;
            set_bits(z, 22, 0+Nia, get_bits(a_m, 26-Nia, 3)); //z[22:0] <= a_m[26:3];
            return z; 
        }else {
            //Denormalised Number
            if (a_e == -127) {
                a_e = -126;
            }else {
                set_bit(a_m, 26-Nia, 1); //a_m[26] <= 1;
            }
            //Denormalised Number
            if (b_e == -127){
                b_e = -126;
            }else{
                set_bit(b_m, 26-Nia, 1);   ///b_m[26] <= 1;
            }
        }
    } 
    //align:
    {    
        if (a_e > b_e) {
            b_e = b_e + 1;
            b_m = (b_m >> 1);
            set_bit(b_m, 0, get_bit(b_m, 0) | get_bit(b_m, 1));//b_m[0] <= b_m[0] | b_m[1];
        }else if (a_e < b_e) {
            a_e = a_e + 1;
            a_m = (a_m >> 1);
            set_bit(a_m, 0, get_bit(a_m, 0) | get_bit(a_m, 1)); //_m[0] <= a_m[0] | a_m[1];
        }
    }

    //add_0:
    { 
        z_e = a_e;
        if (a_s == b_s) {
            sum = a_m + b_m;
            z_s = a_s;
        }else {
            if (a_m >= b_m) {
                sum = a_m - b_m;
                z_s = a_s;
            }else {
                sum = b_m - a_m;
                z_s = b_s;
            }
        }
    }
    //add_1:
    {
        if (get_bit(sum, 27-Nia) == 1) {
            z_m = get_bits(sum, 27-Nia, 4); //z_m <= sum[27:4];
            guard = get_bit(sum, 3); //guard <= sum[3];
            round_bit = get_bit(sum, 2); //round_bit <= sum[2];
            sticky = get_bit(sum,1) | get_bit(sum, 0); //sticky <= sum[1] | sum[0];
            z_e += 1; //<= z_e + 1;
        } else {
            z_m = get_bits(sum, 26 - Nia, 3); //z_m <= sum[26:3];
            guard = get_bit(sum, 2); //guard <= sum[2];
            round_bit = get_bit(sum, 1); //round_bit <= sum[1];
            sticky = get_bit(sum, 0); //sticky <= sum[0];
        }
    }

    //normalise_1:
    {
        if ((get_bit(z_m, 23-Nia) == 0)  && (z_e > -126)) {
            z_e = z_e - 1;
            z_m = (z_m << 1);
            set_bit(z_m, 0, guard); //z_m[0] <= guard;
            guard = round_bit; //guard <= round_bit;
            round_bit = 0;
        }     
    }

    //normalise_2:
    {
        if (z_e < -126) {
            
        cout<<" got to normal 2"<<endl; 
            z_e = z_e + 1;
            z_m = (z_m >> 1);
            guard = get_bit(z_m, 0);//[0];
            round_bit = guard;
            sticky = sticky | round_bit;
        } 
    }

    //round:
    {
        if (guard && (round_bit | sticky | get_bit(z_m, 0))) { 
            
        cout<<"to to rounding"<<endl; 
            z_m = z_m + 1;
            if (z_m == 0xffffff) {
                z_e =z_e + 1;
            }
        }
    }

    //pack:
    {
        cout<<"parts"<<endl; 
        show_binary(get_bits(z_m, 22, 0));
        show_binary(get_bits(z_e, 7, 0) + 127);
        cout<<"parts done"<<endl; 
        set_bits(z, 22, 0 + Nia, get_bits(z_m, 22-Nia, 0)); //z[22 : 0] <= z_m[22:0];
        set_bits(z, 30, 23, get_bits(z_e, 7, 0) + 127); //z[30 : 23] <= z_e[7:0] + 127;
        set_bit(z, 31, z_s); //z[31] <= z_s;
        if (z_e == -126 && (get_bit(z_m, 23 - Nia)==0)) {
            set_bits(z, 30, 23, 0); //z[30 : 23] <= 0;
        }
        //if overflow occurs, return inf
        if (z_e > 127) {
            set_bits(z, 22, 0, 0); //z[22 : 0] <= 0;
            set_bits(z, 30, 23, 255); //z[30 : 23] <= 255;
            set_bit(z, 31, z_s); //z[31] <= z_s;
        }
    }

    return z;

}

//float, float version
/*
float bta::calc(const float &number1, const float &number2) {
    update_energy(Nia, "float", "float"); 
    int RND_BT_TO_DECIDE_ON;
    int num1_mantisa_cut_off;
    int num1_ptr ;
    int mask; 
    memcpy(&num1_ptr, &number1, sizeof(num1_ptr));
    int num1_mantisa =  num1_ptr & ~(0xff800000);
    cout<<"mantisa before approximation"<<bitset<32>(num1_mantisa)<<endl;
    

    //cout<<"mantisa "<<bitset<32>(num1_mantisa)<<endl;
    #ifdef BT_RND 
    mask = 1<< (Nia - 1);
    if (Nia == 0) {
        mask = 0;
    }
    
    
    //cout <<"mask is "<<mask<<endl; 
     
    RND_BT_TO_DECIDE_ON = (num1_mantisa & mask) >> (Nia - 1);
    num1_mantisa_cut_off = (num1_mantisa >> Nia) <<Nia;
    
    if (RND_BT_TO_DECIDE_ON == 1) 
        num1_mantisa = num1_mantisa_cut_off + (1 << Nia);
    else
        num1_mantisa = num1_mantisa_cut_off;
    #else
    num1_mantisa = (num1_mantisa >> Nia) <<Nia;
    #endif 
    cout <<"--num of appx bits: "<< Nia<<endl; 
    cout<<"mantisa after approximation "<<bitset<32>(num1_mantisa)<<endl;
    num1_ptr &= (0xff800000); //get exponent
    num1_ptr |= num1_mantisa; //merge with mantisa
    //cout<<"after rounding"<<bitset<sizeof num1_ptr*8>(*(long unsigned int*)(&num1_ptr))<<endl;
    
    
    int num2_ptr;
    memcpy(&num2_ptr, &number2, sizeof(num2_ptr));
    int num2_mantisa =  num2_ptr & ~(0xff800000);
    int num2_mantisa_cut_off;
    #ifdef BT_RND 
    mask = 1<< (Nia - 1);
    if (Nia == 0) {
        mask = 0;
    }
    RND_BT_TO_DECIDE_ON = (num2_mantisa & mask) >> (Nia - 1);
    num2_mantisa_cut_off = (num2_mantisa >> Nia) <<Nia;
    
    if (RND_BT_TO_DECIDE_ON == 1) 
        num2_mantisa = num2_mantisa_cut_off + (1<<Nia);
    else
        num2_mantisa = num2_mantisa_cut_off;
    #else
    num2_mantisa = (num2_mantisa >> Nia) <<Nia;
    #endif 
    num2_ptr &= (0xff800000);
    num2_ptr |= num2_mantisa;
    

    float num2_restored, num1_restored; 
    memcpy(&num1_restored, &num1_ptr, sizeof(num1_restored));
    memcpy(&num2_restored, &num2_ptr, sizeof(num2_restored));
    
    cout<<"adder output "<<bitset<32>(num2_restored + num1_restored)<<endl;
    return num2_restored + num1_restored;
}
*/


float bta::calc(const double &number1, const double &number2) {
    cout<<"=============insde other half float"<<endl; 
    float numOut = number1; 
    float numOut2 = number2; 
    calc(numOut, numOut2);
}

//int, int version
int bta::calc(const int &a, const int &b) {
    update_energy(Nia, "int", "int"); 
    // inaccurate part
#ifdef VERBOSE 
    cout<<"=============in int version"<<endl; 
    #endif  
    int weight = pow(2, Nia) - 1;
	int iap_a = weight&a;
	int iap_b = weight&b;


#ifdef BT_RND
    int a_op = (iap_a >> (Nia - 1)) == 0x1 ? (a >> Nia) + 1 : (a >> Nia);
    
    //--- a variant calculation of rounding (by first taking abs_value, then rounding, then 
    int a_op_shifted_back = a_op << Nia; 
    //restoring the sign
    /* 
    int a_op_res; //signed restored a (for variant version of raounding)
    int b_op_res; //signed restored b (for variant version of rounding)
    int a_op_abs = (iap_a>> (Nia - 1)) == 0x1 ? (a >> Nia) + 1 : (a >> Nia);
    int b_op_abs = (iap_b>> (Nia - 1)) == 0x1 ? (b >> Nia) + 1 : (b >> Nia);
    if (a <=0) {
       a_op_res = -1*(a_op_abs << Nia);  
    }else{
       a_op_res = (a_op_abs << Nia);  
    }
    */
#else
	int a_op = (a >> Nia);
#endif
#ifdef BT_RND
	int b_op = (iap_b >> (Nia - 1)) == 0x1 ? (b >> Nia) + 1 : (b >> Nia);
    
    int b_op_shifted_back = b_op << Nia; 
    //--- a variant calculation of rounding (by first taking abs_value, then rounding, then 
    //restoring the sign
    /* 
    if (b <=0) {
       b_op_res = -1*(b_op_abs << Nia);  
    }else{
       b_op_res = (b_op_abs << Nia);  
    }
    */
#else
	int b_op = (b >> Nia);
#endif


    //variant version of rounding calculation 
    //int tmp_variant =  (b_op_shifted_back+a_op_shifted_back);
    int tmp_sg_version =   ((a_op) + (b_op)) << Nia; //tmp seogoo version
    //cout<<"un absed version: "<< tmp_variant<<endl;
    //cout <<"absed version: " << tmp_sg_version<<endl;
    //assert(tmp_variant == tmp_sg_version); 
    

    return ((a_op) + (b_op)) << Nia;
}


unsigned int bta::calc(const unsigned int &a, const unsigned int &b) {
    update_energy(Nia, "int", "int"); 
    #ifdef BT_RND
       printf("ERRR: rounding not defined for unsigned int unsigned int bta \n");
       exit(0);
    #endif
 

    
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
    
    update_energy(Nia, "int", "int"); 
    
    #ifdef BT_RND
       printf("ERRR: rounding not defined for unsigned int, int bta \n");
       exit(0);
    #endif
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
    update_energy(Nia, "int", "int"); 
    // inaccurate part
    
    #ifdef BT_RND
       printf("ERRR: rounding not defined for int, unsigned int bta \n");
       exit(0);
    #endif

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
    update_energy(Nia, "int", "int"); 
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
