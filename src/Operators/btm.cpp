#include <iostream>
#include <complex>
#include <cassert>
#include <vector>
#include "btm.h"
#include "fp_helpers.h"
#include "globals.h"
#include <string>
#include <cstring>
#include <vector>
using namespace std;
#include <cstring>
extern long double energy_value;

btm::btm(void) {}
//void btm::update_energy(int n_apx_bits){
//    energy_value += 31* (32 - n_apx_bits) + 10;
//}



//vector<float> mul_long_long_energy_vals2 {0, 17.6200, 16.9703, 16.5727, 16.0470, 15.4340};

vector<float> mul_long_long_energy_vals {17.9, 17.6200, 16.9703, 16.5727, 16.0470, 15.4340,  15.0166,14.5268 ,13.9600 ,13.6053 ,13.1328 ,12.6118 ,12.3106 ,11.8315 , 11.2906, 10.9915};
vector<float> mul_long_int_energy_vals {8.8, 8.5007, 8.0576 , 7.6706 , 7.3762 , 6.9593 , 6.56237,6.2935 ,5.9425 ,5.5465 ,5.3194, 4.9607 ,4.6345, 4.4028 ,4.1278 ,3.7874};
vector<float> mul_int_int_energy_vals {4.6, 4.4194, 4.1470, 3.8712, 3.6900, 3.4301,3.1957 ,3.0342 ,2.8028 ,2.5685 ,2.4261,2.558612,2.0411,1.9182,1.7561,1.5972};
//--- their counters
extern vector<int> mul_long_long_energy_counters;
extern vector<int> mul_long_int_energy_counters; 
extern vector<int> mul_int_int_energy_counters;

void btm::update_energy(int n_apx_bits, string op1_type, string op2_type){
    /* 
    cout <<energy_value<<endl; 
    cout<<mul_long_long_energy_vals[n_apx_bits]<<endl;
    cout<<energy_value+mul_long_long_energy_vals[n_apx_bits]<<endl;
     */
    if (op1_type ==  "long" && op2_type ==  "long") {
        energy_value += mul_long_long_energy_vals[n_apx_bits];
        mul_long_long_energy_counters[n_apx_bits] +=1;
    }
    else if (op1_type=="int" && op2_type =="long") {
        energy_value += mul_long_int_energy_vals[n_apx_bits];
        mul_long_int_energy_counters[n_apx_bits] +=1;
    }
    else if (op1_type == "long" && op2_type == "int") {
        energy_value += mul_long_int_energy_vals[n_apx_bits];
        mul_long_int_energy_counters[n_apx_bits] +=1; 
    }
    else if (op1_type == "int" && op2_type== "int") {
        energy_value += mul_int_int_energy_vals[n_apx_bits];
        mul_int_int_energy_counters[n_apx_bits] +=1; 
    }
    else {
        cout<<"the energy value for this bta types is not defined"<<endl;
        //exit(0);
    }
    //energy_valuee+= (32 - n_apx_bits) + 10;
}



btm::btm(size_t Nt, size_t vbl, bool table_gen) {
    this->Nt = Nt;
    this->msb = vbl-1;
    this->lsb = 0;
    this->vbl = vbl;
    this->hbl = vbl;

    if (table_gen) tbl_gen();
}

size_t btm::get_ianum_bits(void) {
	return this->vbl;
}

btm::~btm(void) {}

size_t btm::get_hbl_bits(void) {
    return hbl;
}


size_t btm::get_vbl_bits(void) {
    return vbl;
}
//long, long version
int btm::calc(const long &a, const long &b) {
    update_energy(vbl, "long", "long"); 
    

    // inaccurate part
    int weight = pow(2, vbl) - 1;
    long abs_a = (a<0) ? -a : a;
    long abs_b = (b<0) ? -b : b;
    int sign = (a<0 && b>0) || (a>0 && b<0) ? 1 : 0;
    int iap_a = weight&a;
    int iap_b = weight&b;

#ifdef BT_RND
    int a_op = (iap_a>> (vbl - 1)) == 0x1 ? (abs_a >> vbl) + 1 : (abs_a >> vbl);
#else
    int a_op = (abs_a >> vbl);
#endif

#ifdef BT_RND
    int b_op = (iap_b>> (vbl - 1)) == 0x1 ? (abs_b >> vbl) + 1 : (abs_b >> vbl);
#else
    int b_op = (abs_b >> vbl);
#endif

    //printf("SGLEE VBL: %d, %d, %d\n", a_op, b_op, ((a_op)*(b_op)) << (2*vbl));
    int tmp = ((a_op)*(b_op)) << (2*vbl);
    // accurate part
    return (sign ? -tmp : tmp);
}

//long, int version
int btm::calc(const long &a, const int &b) {
    update_energy(vbl, "long", "int"); 
    

    // inaccurate part
    int weight = pow(2, vbl) - 1;
    long abs_a = (a<0) ? -a : a;
    long abs_b = (b<0) ? -b : b;
    int sign = (a<0 && b>0) || (a>0 && b<0) ? 1 : 0;
    int iap_a = weight&a;
    int iap_b = weight&b;

#ifdef BT_RND
    int a_op = (iap_a>> (vbl - 1)) == 0x1 ? (abs_a >> vbl) + 1 : (abs_a >> vbl);
#else
    int a_op = (abs_a >> vbl);
#endif

#ifdef BT_RND
    int b_op = (iap_b>> (vbl - 1)) == 0x1 ? (abs_b >> vbl) + 1 : (abs_b >> vbl);
#else
    int b_op = (abs_b >> vbl);
#endif

    //printf("SGLEE VBL: %d, %d, %d\n", a_op, b_op, ((a_op)*(b_op)) << (2*vbl));
    int tmp = ((a_op)*(b_op)) << (2*vbl);
    // accurate part
    return (sign ? -tmp : tmp);
}


//int, long version
int btm::calc(const int &a, const long &b) {
    update_energy(vbl, "int", "long"); 
    
    
    // inaccurate part
    int weight = pow(2, vbl) - 1;
    long abs_a = (a<0) ? -a : a;
    long abs_b = (b<0) ? -b : b;
    int sign = (a<0 && b>0) || (a>0 && b<0) ? 1 : 0;
    int iap_a = weight&a;
    int iap_b = weight&b;


#ifdef BT_RND
    int a_op = (iap_a>> (vbl - 1)) == 0x1 ? (abs_a >> vbl) + 1 : (abs_a >> vbl);
#else
    int a_op = (abs_a >> vbl);
#endif

#ifdef BT_RND
    int b_op = (iap_b>> (vbl - 1)) == 0x1 ? (abs_b >> vbl) + 1 : (abs_b >> vbl);
#else
    int b_op = (abs_b >> vbl);
#endif

    //printf("SGLEE VBL: %d, %d, %d\n", a_op, b_op, ((a_op)*(b_op)) << (2*vbl));
    int tmp = ((a_op)*(b_op)) << (2*vbl);
    // accurate part
    return (sign ? -tmp : tmp);
}

float btm::calc(const float &number1, const int &number2) {
    float numOut = number2; 
    calc(number1, numOut);
} 

float btm::calc(const int &number1, const float &number2) {
    cout<<"=============insde other half float"<<endl; 
    float numOut = number1; 
    calc(numOut, number2);
} 


//float, float version
float btm::calc(const float &number1, const float &number2) {
  //update_energy(vbl, "float", "float"); 

  int a ;
  int b ;
  float z = 0; //intermediate output used in the function
  int output = 0;  //output to return
  memcpy(&a, &number1, sizeof(a));
  memcpy(&b, &number2, sizeof(b));

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
  //----------------------------------------------------------------- 
  long product;


#ifdef BT_RND 
    a_m = get_bits(a, 22, 0 + vbl);
    b_m = get_bits(b, 22, 0 + vbl);
#else
    a_m = get_bits(a, 22, 0 + vbl);
    b_m = get_bits(b, 22, 0 + vbl);
#endif
    a_e = get_bits(a, 30, 23) - 127;
    b_e = get_bits(b, 30, 23) - 127;
    a_s = get_bit(a, 31);
    b_s = get_bit(b, 31);

    
    
      //special_cases:
    {   
        //if a is NaN or b is NaN return NaN 
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
        }   
        //if b is zero return NaN
        else if (b_e == -127 && b_m == 0) {
            set_bit(z, 31, 1);
            set_bits(z, 30, 23, 255);
            set_bit(z, 22, 1); 
            set_bits(z, 21, 0 , 0);
            return z; 
        }
        //if b is inf return inf
        else if (b_e == 128) {
          set_bit(z, 31, a_s ^ b_s);
          set_bits(z, 30, 23, 255); //z[30:23] <= 255;
          set_bits(z, 22, 0, 0); //z[22:0] <= 0;
          return z; 
        //if a is zero return zero
        } else if (a_e == -127 && a_m == 0){
          set_bit(z, 31, a_s ^ b_s);
          set_bits(z, 30, 23, 0);
          set_bits(z, 22, 0, 0); 
          return z; 
        //if b is zero return zero
         } else if (b_e == -127 && b_m == 0) {
          set_bit(z, 31, a_s ^ b_s); //z[31] <= a_s ^ b_s;
          set_bits(z, 30, 23, 0); //z[30:23] <= 0;
          set_bits(z, 22, 0, 0); //z[22:0] <= 0;
          return z; 
         }else {
            //Denormalised Number
            if (a_e == -127) {
                a_e = -126;
            }else {
                set_bit(a_m, 23-vbl, 1); //a_m[26] <= 1;
            }
            //Denormalised Number
            if (b_e == -127){
                b_e = -126;
            }else{
                set_bit(b_m, 23-vbl, 1);   ///b_m[26] <= 1;
            }
         }
    }

    //normalise_a:
    {
        while (get_bit(a_m, 23 - vbl) != 1) {
          a_m = (a_m << 1);
          a_e = (a_e - 1);
        }
    }

    //normalise_b:
    { 
        while (get_bit(b_m, 23 - vbl) != 1) {
                b_m = (b_m << 1);
                b_e = (b_e - 1);
        }
    }

        
    //multiply_0:
    {
        z_s = a_s ^ b_s;
        z_e = a_e + b_e + 1;
        //product <= a_m[23-vbl:0] * b_m[23-vbl: 0] * 4;
        product = (long)get_bits(a_m, 23-vbl , 0) * (long)get_bits(b_m, 23-vbl, 0) * 4;
    }
    
    //show_hex(z_m);

    //multiply_1:
    {
        z_m = get_bits(product, 49-2*vbl, 26-vbl);
        guard = get_bit(product, 25-vbl);
        round_bit = get_bit(product, 24-vbl);
        sticky = get_bits(product, 23-vbl, 0) != 0;
    }
    
    
    //normalise_1:
    {
        while (get_bit(z_m, 23-vbl) == 0){
          z_e = z_e - 1;
          z_m = (z_m << 1);
          set_bit(z_m, 0,  guard);
          guard = round_bit;
          round_bit = 0;
        }
     }
     
    
    //    show_hex(a_m);
//    show_hex(b_m);
//    show_hex(z_m);

    // normalise_2:
    { 
        while (z_e < -126) {
          z_e = z_e + 1;
          int old_guard = guard; 
          guard = get_bit(z_m, 0);
          z_m = z_m >> 1;
          int old_round_bit = round_bit; 
          round_bit = old_guard;
          sticky = sticky | old_round_bit;
        }
    }
    
    //round:
    {
        if (guard && (round_bit | sticky | get_bit(z_m, 0))) { 
            
            z_m = z_m + 1;
            if (z_m == 0xffffff) {
                z_e =z_e + 1;
            }
        }
    }

    //pack:
    {
        set_bits(z, 22, 0 + vbl, get_bits(z_m, 22-vbl, 0)); //z[22 : 0] <= z_m[22:0];
        set_bits(z, 30, 23, get_bits(z_e, 7, 0) + 127); //z[30 : 23] <= z_e[7:0] + 127;
        set_bit(z, 31, z_s); //z[31] <= z_s;
        if (z_e == -126 && (get_bit(z_m, 23 - vbl)==0)) {
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



//float btm::calc(const float &number1, const float &number2) {
//    
//    #ifdef BT_RND
//       printf("ERRR: rounding not defined for float,float btm \n");
//       exit(0);
//    #endif
//    
//    /*
//    FILE* fp;
//    fp = fopen("diff_file.txt", "ab+"); 
//    
//    if ( num1_inverse_converted*num2_inverse_converted != (number1*number2)){
//        float diff_part_1 =  num1_inverse_converted*num2_inverse_converted;
//        float diff_part_2 =  number1*number2;
//        float diff = (diff_part_1 - diff_part_2);
//        
//        //--checking for under/over-flow 
//        if (std::isinf(diff_part_1)) {
//            fprintf(fp, "par_1_overflow\n");
//        }
//        if (std::isinf(diff_part_2)) {
//            fprintf(fp, "par_2_overflow\n");
//        }
//        if ((diff_part_1 != diff_part_2) && (diff ==0)){
//            fprintf(fp, "diff underflow\n");
//        }
//        fprintf(fp, "error   ");
//        if ( diff > 1){
//            fprintf(fp, "acc:%f apx: %f diff:%f\n",num1_inverse_converted*num2_inverse_converted ,number1*number2, diff); 
//        }
//        fprintf(fp, "------\n");
//    }
//    
//    fclose(fp);
//    */ 
//    
//    /*     
//    int *num1_ptr = (int *)malloc(sizeof(int));
//    memcpy(num1_ptr, &number1, sizeof(num1_ptr));
//    int num1_mantisa =  *num1_ptr & ~(0xff800000);
//    num1_mantisa = (num1_mantisa >> vbl) <<vbl;
//    *num1_ptr &= (0xff800000);
//    *num1_ptr |= num1_mantisa;
//    
//    int *num2_ptr = (int *)malloc(sizeof(int));
//    memcpy(num2_ptr, &number2, sizeof(num2_ptr));
//    int num2_mantisa =  *num2_ptr & ~(0xff800000);
//    num2_mantisa = (num2_mantisa >> vbl) <<vbl;
//    *num2_ptr &= (0xff800000);
//    *num2_ptr |= num2_mantisa;
//    */
//
//    update_energy(vbl, "float", "float"); 
//    int num1_ptr;
//    memcpy(&num1_ptr, &number1, sizeof(num1_ptr));
//    int num1_mantisa =  num1_ptr & ~(0xff800000);
//    num1_mantisa = (num1_mantisa >> vbl) <<vbl;
//    num1_ptr &= (0xff800000);
//    num1_ptr |= num1_mantisa;
//    
//    int num2_ptr; 
//    memcpy(&num2_ptr, &number2, sizeof(num2_ptr));
//    int num2_mantisa =  num2_ptr & ~(0xff800000);
//    num2_mantisa = (num2_mantisa >> vbl) <<vbl;
//    num2_ptr &= (0xff800000);
//    num2_ptr |= num2_mantisa;
//
//
//    
//    float num2_restored, num1_restored; 
//    memcpy(&num1_restored, &num1_ptr, sizeof(num1_restored));
//    memcpy(&num2_restored, &num2_ptr, sizeof(num2_restored));
//    return num1_restored * num2_restored;
//   /* 
//    fpType num1;
//    fpType num2;
//    getFPComponents(number1, num1); //get the fp componenets
//    getFPComponents(number2, num2); //get the fp components
//
//    num1.Mantisa = ((num1.Mantisa)>> vbl) <<vbl;
//    num2.Mantisa = ((num2.Mantisa)>> vbl) <<vbl;
//    
//    float num1_inverse_converted = convertFPCompToFP(num1);
//    float num2_inverse_converted = convertFPCompToFP(num2);
//    
//    if (num1_inverse_converted != num1_restored){
//        cout<<"main: " <<number1<<"inverse: "<<num1_inverse_converted<< " num1_ptr: "<< num1_ptr << "restored :"<<num1_restored<<endl;
//        exit(0); 
//    }
//    if (num2_inverse_converted != num2_restored){
//        cout<<"inverse: "<<num2_inverse_converted<< " num2_ptr: "<<num2_restored<<endl;
//        exit(0); 
//    }
//    return num1_inverse_converted * num2_inverse_converted;
//    */
//}



float btm::calc(const double &number1, const double &number2) {
    cout<<"=============insde other half float"<<endl; 
    float numOut = number1; 
    float numOut2 = number2; 
    calc(numOut, numOut2);
}


//int, int version
int btm::calc(const int &a, const int &b) {
   update_energy(vbl, "int", "int");    
#ifdef VERBOSE 
    cout<<"=============in int version"<<endl; 
    #endif 
    int weight = pow(2, vbl) - 1;
    int iap_a = weight&a;
    int iap_b = weight&b;


#ifdef BT_RND
    int a_op = (iap_a>> (vbl - 1)) == 0x1 ? (a >> vbl) + 1 : (a >> vbl);
    int a_op_shifted_back = a_op <<vbl;
#else
    int a_op = (a >> vbl);
    int a_op_shifted_back = a_op <<vbl;
#endif


#ifdef BT_RND
    int b_op = (iap_b>> (vbl - 1)) == 0x1 ? (b >> vbl) + 1 : (b >> vbl);
    int b_op_shifted_back = b_op <<vbl;
    
   #else
    int b_op = (b >> vbl);
    int b_op_shifted_back = b_op <<vbl;
#endif
    //int tmp = ((a_op)*(b_op)) << (2*vbl);
    //assert(((b_op_not_abs * a_op_not_abs) <<(2*vbl)) == tmp_sg_version );
    //assert(tmp == a_ops_shifted_back*b_ops_shifted_back);
    return b_op_shifted_back * a_op_shifted_back;
}


unsigned int btm::calc(const unsigned int &a, const unsigned int &b) {
   #ifdef BT_RND
       printf("ERRR: rounding not defined for unsigned int,unsigned int\n");
       exit(0);
    #endif

    
    update_energy(vbl, "int" ,"int");    
#ifdef VERBOSE 
    cout<<"=============in unsigned int version"<<endl; 
    #endif 
    // inaccurate part
    unsigned int weight = pow(2, vbl) - 1;
    unsigned int abs_a =  a;
    unsigned int abs_b =  b;

#ifdef BT_RND
    unsigned int a_op = (abs_a >> (vbl - 1)) == 0x1 ? (abs_a >> vbl) + 1 : (abs_a >> vbl);
#else
    unsigned int a_op = (abs_a >> vbl);
#endif

#ifdef BT_RND
    unsigned int b_op = (abs_b >> (vbl - 1)) == 0x1 ? (abs_b >> vbl) + 1 : (abs_b >> vbl);
#else
    unsigned int b_op = (abs_b >> vbl);
#endif

    //prunsigned intf("SGLEE VBL: %d, %d, %d\n", a_op, b_op, ((a_op)*(b_op)) << (2*vbl));
    unsigned int tmp = ((a_op)*(b_op)) << (2*vbl);
    // accurate part
    return tmp;
}

int btm::calc(const unsigned int &a_unsigned, const int &b) {
   update_energy(vbl, "int", "int");    

   #ifdef BT_RND
       printf("ERRR: rounding not defined for unsigned int,int\n");
       exit(0);
    #endif

#ifdef VERBOSE 
    cout<<"=============in half usigned int version"<<endl; 
    #endif 
    int a = (int) a_unsigned ;
    // inaccurate part
    int weight = pow(2, vbl) - 1;
    int abs_a =  a;
    int abs_b =  b;

#ifdef BT_RND
    int a_op = (abs_a >> (vbl - 1)) == 0x1 ? (abs_a >> vbl) + 1 : (abs_a >> vbl);
#else
    int a_op = (abs_a >> vbl);
#endif

#ifdef BT_RND
    int b_op = (abs_b >> (vbl - 1)) == 0x1 ? (abs_b >> vbl) + 1 : (abs_b >> vbl);
#else
    int b_op = (abs_b >> vbl);
#endif

    //printf("SGLEE VBL: %d, %d, %d\n", a_op, b_op, ((a_op)*(b_op)) << (2*vbl));
    int tmp = ((a_op)*(b_op)) << (2*vbl);
    // accurate part
    return tmp;
}

int btm::calc(const int &a, const unsigned int &b_unsigned) {
   update_energy(vbl, "int", "int");    

    #ifdef BT_RND
       printf("ERRR: rounding not defined for unsigned int,unsigned int\n");
       exit(0);
    #endif

#ifdef VERBOSE 
    cout<<"=============in half usigned int version"<<endl; 
    #endif 
    int b = (int) b_unsigned;
    // inaccurate part
    int weight = pow(2, vbl) - 1;
    int abs_a =  a;
    int abs_b =  b;

#ifdef BT_RND
    int a_op = (abs_a >> (vbl - 1)) == 0x1 ? (abs_a >> vbl) + 1 : (abs_a >> vbl);
#else
    int a_op = (abs_a >> vbl);
#endif

#ifdef BT_RND
    int b_op = (abs_b >> (vbl - 1)) == 0x1 ? (abs_b >> vbl) + 1 : (abs_b >> vbl);
#else
    int b_op = (abs_b >> vbl);
#endif

    //printf("SGLEE VBL: %d, %d, %d\n", a_op, b_op, ((a_op)*(b_op)) << (2*vbl));
    int tmp = ((a_op)*(b_op)) << (2*vbl);
    // accurate part
    return tmp;
}



int btm::calc_ref(const int &a, const int &b) {
   update_energy(vbl, "int", "int");    
    return a*b;
}

void btm::tbl_gen() {
    int i, j;
    int i_w, j_w;
    for (i = 0; i < pow(2, msb - lsb + 1); i++) {
        for (int j = 0; j < pow(2, msb - lsb + 1); j++) {
            if (!(i == 0 && j == 0)) {
                err_tbl.push_back(make_pair(make_pair((0x80000000 | i), (0x80000000 | j)), make_pair(make_pair(j, i), i*j)));
            }
        }
    }
}
