/**
* @file RecME.cpp
* @author Muhammad Usman Karim Khan
* Group: Prof. Joerg Henkel at Chair for Embedded Systems (CES), KIT
* @brief This file contains the computational adaptation for both number
* of threads and the frequency of the cores.
*/
#include "Operators.h"
#include "Utilities.h"
#include "RecME.h"
#include "operatorFile_parser.h"
#include "setSubType.h"
#define		BLK_SIZE		8						//!< Default Blk size
#define		SW_WIDTH		32						//!< Default SW width
#define		SW_HEIGHT		32						//!< Default SW height
#define appx

//    ACINT a = 46;
//	ACINT b = 38;
//	size_t Nt = 16;//total number of bits
//	size_t Nia = 6;//total number of apx bits starting from 0
//	size_t msb = Nia-1;
//	size_t lsb = 0;
//	size_t hbl = Nia; //some type of apx 
//	size_t vbl = hbl; // some type of apx
//	size_t op_type = 2; // '1' for adder, '2' for multiplier
//
//    eta1 add1(Nt, Nia, msb, lsb, 1);
//	bam mul1(Nt,  hbl, vbl,  hbl-1,  0, 1);
//    
    vector<vector<string> > OpTypeVec;
    string OpListFile= "../input_output_text_files/sample_op_list.txt";
    enum status {SUCCESS, FAILURE}; 
    hw_ac **myOp;   
//loa y0(Nt, Nia, msb, lsb, 1);
    //eta2 x1(Nt, K, msb, lsb);
	//bta y0(Nt, Nia, msb, lsb, 1);

//#endif


RecME::RecME(i32 iID, i32 iImgWidth, i32 iImgHeight, i32 iImgStride, i32 iBlkSize, i32 iSWWidth, i32 iSWHeight, i32 iSearchStrength):
	m_iID(iID), m_iImgWidth(iImgWidth), m_iImgHeight(iImgHeight), m_iImgStride(iImgStride),m_iSearchStrength(iSearchStrength)
{
	m_iBlkSize = (iBlkSize < 1 ? BLK_SIZE : iBlkSize);
	m_iSWWidth = min((iSWWidth < 1 ? SW_WIDTH : iSWWidth), 256);		// 8-bit MV
	m_iSWHeight = min((iSWHeight < 1 ? SW_HEIGHT : iSWHeight), 256);	// 8-bit MV

	// Only utilize a square search window for now.
	// Make the search window of odd size to have a mid-point
	m_iSWWidth = max(m_iSWWidth,m_iSWHeight) | 0x1;
	m_iSWHeight = max(m_iSWWidth,m_iSWHeight) | 0x1;

	m_iImgWidthInBlks = m_iImgWidth/m_iBlkSize;
	m_iImgHeightInBlks = m_iImgHeight/m_iBlkSize;
	m_iBlksPerFrame = m_iImgWidthInBlks*m_iImgHeightInBlks;

	m_ppbMVRightToLeft[0] = new i8[m_iBlksPerFrame];
	m_ppbMVRightToLeft[1] = new i8[m_iBlksPerFrame];

	m_piSAD = new i32[m_iBlksPerFrame];
}

i32 RecME::BlockDiff(byte *pbInput0, i32 iStride0, byte *pbInput1, i32 iStride1, i32 iBlockSize, i32 iSkipPel)
{
	
        
//    for (int i = 0; i<OpTypeVec.size(); i++) {
//      int result = myOp[i]->calc(var1, var2); 
//        printf("this is the return value %d\n", result);
//    }
//
    byte *pbIn0, *pbIn1;
	i32 iSAD = 0;
	for(i32 y=0;y<iBlockSize;y+=(1+iSkipPel))
	{
		m_iNumSADs++;
//        pbIn0 = (myOp[0]->calc_ref(pbInput0, y*iStride0);
//        pbIn1 = myOp[1]->calc_ref(pbInput1, y*iStride0);
		pbIn0 = pbInput0 + y*iStride0;
		pbIn1 = pbInput1 + y*iStride0;
        for(i32 x=0;x<iBlockSize;x+=(1+iSkipPel)){
            i32 iSADtemp = ABS(myOp[2]->calc(i32(pbIn0[x]), -1*i32(pbIn1[x]))); //AdditionOp 
            iSAD = myOp[3]->calc(iSAD, iSADtemp);	//AdditionOp 
        }
     }	
    return iSAD;
}

i32 RecME::GetMinSADPt(byte *pbInputBlk, i32 iBlkStride, i32 iBlkSize, byte *pbSearchWin, 
							  i32 iSWWidth, i32 iSWHeight, i32 iSWStride, i32 & iMinPtX, i32 & iMinPtY)
{
 #define		COMPUTE_SAD																		\
	do{																						\
		pbRefBlk = pbSearchWin+y*iSWStride+x;												\
		iSAD = BlockDiff(pbInputBlk,iBlkStride,pbRefBlk,iSWStride,iBlkSize,0);				\
		iNumSADs++;																			\
		if(iSAD <= iMinSAD)																	\
		{																					\
			iMinPtX = x;																	\
			iMinPtY = y;																	\
			iMinSAD = iSAD;																	\
		}																					\
	}while(0)

//#define		COMPUTE_SAD																		\
//	do{																						\
//		pbRefBlk = myOp[4]->calc(myOp[5]->calc(pbSearchWin,y*iSWStride),x);												\
//		iSAD = BlockDiff(pbInputBlk,iBlkStride,pbRefBlk,iSWStride,iBlkSize,0);				\
//		iNumSADs++;																			\
//		if(iSAD <= iMinSAD)																	\
//		{																					\
//			iMinPtX = x;																	\
//			iMinPtY = y;																	\
//			iMinSAD = iSAD;																	\
//		}																					\
//	}while(0)
//

	i32 iSAD;
	i32 iMinSAD = 99999999;
	byte *pbRefBlk;
	i32 iNumSADs = 0;

	for(i32 y=0;y<iSWHeight;y++)
	{
		for(i32 x=0;x<iSWWidth;x++)
		{
			COMPUTE_SAD;
		}
	}

	MAKE_SURE(iMinPtX >=0 && iMinPtX < iSWWidth && iMinPtY >= 0 && iMinPtY < iSWHeight, 
		"Error: The minimum point is outside the window");
	return iMinSAD;
}

void RecME::GenerateMVs(byte *pbRefFrame, byte *pbCurrFrame, 
	i32 iPelsAvailLeft, i32 iPelsAvailRight, i32 iPelsAvailTop, i32 iPelsAvailBottom)
{
	i32 iSWMinX, iSWMaxX, iSWMinY, iSWMaxY, iSWWidth, iSWHeight, iMinPtX, iMinPtY;
	i32 x,y;
	i32 iPelMinX = -iPelsAvailLeft;
	i32 iPelMinY = -iPelsAvailTop;
	i32 iPelMaxX = myOp[6]->calc(m_iImgWidth,iPelsAvailRight);
	i32 iPelMaxY = myOp[7]-> calc(m_iImgHeight,iPelsAvailBottom);
	i32 iBlkNum = 0;
	i32 iStartMVX, iStartMVY;

	y = 0;
	x = 0;
	for(i32 i=0;i<m_iImgHeightInBlks;i++,x=0,y+=m_iBlkSize)
	{
		for(i32 j=0;j<m_iImgWidthInBlks;j++,iBlkNum++,x+=m_iBlkSize)
		{
			// Estimate the start MV in the search window for the motion estimation
			// Currently its 0, but it can be a better guess (like PMV in H.264)
			iStartMVX = 0;
			iStartMVY = 0;
			
			// Search window is around the predicted MV
			iSWMinX = max(myOp[8]->calc(myOp[9]->calc(x,iStartMVX),-1*m_iSWWidth/2),iPelMinX);
			iSWMinY = max(myOp[10]->calc(myOp[11]->calc(y,iStartMVY), -1*m_iSWHeight/2),iPelMinY);
			iSWMaxX = min(myOp[12]->calc(myOp[13]->calc(x,iStartMVX), m_iSWWidth/2),myOp[14]->calc(iPelMaxX,-1*m_iBlkSize));
			iSWMaxY = min(myOp[15]->calc(myOp[16]->calc(y,iStartMVY),m_iSWHeight/2),myOp[17]->calc(iPelMaxY,-1*m_iBlkSize));
			iSWWidth = myOp[18]->calc(iSWMaxX,-1*iSWMinX)+1;
			iSWHeight = myOp[19]->calc(iSWMaxY,-1*iSWMinY)+1;

			// Starting search point in the search window
			iMinPtX = myOp[20]->calc(myOp[21]->calc(x,iStartMVX),-1*iSWMinX);
			iMinPtY = myOp[22]->calc(myOp[23]->calc(y,iStartMVY), -1*iSWMinY);

			// Get the minimum point SAD inside the search window.
            m_piSAD[iBlkNum] = GetMinSADPt(&pbCurrFrame[y*m_iImgStride+x],m_iImgStride,m_iBlkSize, &pbRefFrame[iSWMinY*m_iImgStride+iSWMinX],
				iSWWidth,iSWHeight,m_iImgStride,iMinPtX,iMinPtY);

			// Generate the MV, from the current frame to the reference frame
			m_ppbMVRightToLeft[0][iBlkNum] = myOp[24]->calc(myOp[25]->calc(iSWMinX,iMinPtX),-1*x);
			m_ppbMVRightToLeft[1][iBlkNum] = myOp[26]->calc(myOp[27]->calc(iSWMinY,iMinPtY),-1*y);
		}
	}
}

void RecME::MotionEstimation(byte *pbLeftFrame, byte *pbRightFrame, i32 iPelsAvailLeft, i32 iPelsAvailRight,
		i32 iPelsAvailTop, i32 iPelsAvailBottom)
{
	
    int status = operatorFile_parser(OpListFile, OpTypeVec);
    
    //defiing an array of MyOps 
    myOp = new hw_ac*[OpTypeVec.size()];
    //instantiating the array elements to the values of OpTypeVec 
    //note: OpTypeVec is populated with the parsed values in the OpListFile 
    for (int i = 0; i<OpTypeVec.size(); i++) {
        int status = setOpSubTypeAndInputs(&myOp[i], OpTypeVec[i]);
        if (status == FAILURE) {
            printf("this type is not acceptable \n"); 
            return;// 0;
        }
    }
//       for (int i =0; i < OpTypeVec.size(); i++){ 
//           cout<<"inptu size"<<  OpTypeVec.size();
//           vector<string> inputTypes = OpTypeVec[i]; 
//     for (int j =0; j <inputTypes.size(); j++) {
//        cout<< inputTypes[j]<<endl;
//      } 
//      cout <<endl; 
//    }
//    cout<<"done here"<<endl;
//

    m_iNumSADs = 0;
	m_uiTime = GetTimeInMiliSec();

	// Generate the motion vectors from the right to the left frame.
	// Use only the first channel
	GenerateMVs(pbLeftFrame, pbRightFrame, iPelsAvailLeft, iPelsAvailRight, iPelsAvailTop, iPelsAvailBottom);
	m_uiTime = GetTimeInMiliSec()-m_uiTime;

   OpTypeVec.erase(OpTypeVec.begin(), OpTypeVec.end()); 
}

void RecME::GetMV(i8 **pbMVX, i8 **pbMVY)
{
	*pbMVX = m_ppbMVRightToLeft[0];
	*pbMVY = m_ppbMVRightToLeft[1];
}

void RecME::GetMV(i32 iBlkIdx, i8 & iMVX, i8 & iMVY)
{
	iMVX = m_ppbMVRightToLeft[0][iBlkIdx];
	iMVY = m_ppbMVRightToLeft[1][iBlkIdx];
}

void RecME::GetMV(i32 iX, i32 iY, i8 & iMVX, i8 & iMVY)
{
	i32 iBlkIdx = iY/m_iBlkSize*m_iImgWidthInBlks + iX/m_iBlkSize;
	iMVX = m_ppbMVRightToLeft[0][iBlkIdx];
	iMVY = m_ppbMVRightToLeft[1][iBlkIdx];
}

RecME::~RecME()
{
	delete [] m_ppbMVRightToLeft[0];
	delete [] m_ppbMVRightToLeft[1];
	delete [] m_piSAD;
}
