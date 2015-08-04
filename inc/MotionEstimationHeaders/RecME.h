/**
* @file RecME.h
* @author Muhammad Usman Karim Khan
* Group: Prof. Joerg Henkel at Chair for Embedded Systems (CES), KIT
* @brief This file contains the class for motion estimation algorithm.
*/

#ifndef __RECME_H__
#define __RECME_H__

#include "TypeDefs.h"

/**
*	RecME.
*	Recursive motion estimation class.
*/
class RecME
{
protected:
	i32					m_iSWWidth;					//!< Width of the search window
	i32					m_iSWHeight;				//!< Height of the search window
	i32					m_iImgWidth;				//!< Width of the image
	i32					m_iImgHeight;				//!< Height of the image
	i32					m_iImgStride;				//!< Stride of the image
	i32					m_iBlkSize;					//!< Width/height of a block in the image
	u32					m_uiTime;					//!< Time consumed for processing a frame
	i32					m_iBlksPerFrame;			//!< Total blocks per frame.
	i32					m_iImgWidthInBlks;			//!< Total blocks in the width of the frame.
	i32					m_iImgHeightInBlks;			//!< Total blocks in the height of the frame.
	i8					*m_ppbMVRightToLeft[2];		//!< Motion vectors [x][y]. x is increasing from left to right and y from top to bottom. Always from the right frame to the left frame.
	i32					*m_piSAD;					//!< SAD of the motion vectors.
	i32					m_iNumSADs;					//!< Number of SADs performed for the complete frame
	i32					m_iSearchStrength;			//!< Strength of ME, from lowest (1) to highest (10)
	i32					m_iID;						//!< ID for ID purposes
	/**
	*	Difference between blocks.
	*	Get the difference between two input square blocks of the same size.
	*	@return SAD between the blocks
	*/
	i32			BlockDiff(byte *pbInput0, i32 iStride0, byte *pbInput1, i32 iStride1, i32 iBlockSize, i32 iSkipPel);

		/**
	*	Get the point of minimum difference.
	*	The Min difference point is from the top left of the search window.
	*	@param iMinPtX Starting search point in x-direction (updated)
	*	@param iMinPtY Starting search point in y-direction (updated)
	*	@return SAD between the input and the most correlated block.
	*/
	i32			GetMinSADPt(byte *pbInputBlk, i32 iBlkStride, i32 iBlkSize, byte *pbSearchWin, 
		i32 iSWWidth, i32 iSWHeight, i32 iSWStride, i32 & iMinPtX, i32 & iMinPtY);

	/**
	*	Generate MVs.
	*	This will generate MVs from the right to the left frame.
	*/
	void		GenerateMVs(byte *pbRefFrame, byte *pbCurrFrame, i32 iPelsAvailLeft, i32 iPelsAvailRight, i32 iPelsAvailTop, i32 iPelsAvailBottom);


public:
	RecME(){}
	RecME(i32 iID, i32 iImgWidth, i32 iImgHeight, i32 iImgStride, i32 iBlkSize, i32 iSWWidth, i32 iSWHeight, i32 iSearchStrength);
	~RecME();

	/**
	*	Motion Estimation.
	*	Generates the motion vectors.
	*/
	void MotionEstimation(byte *pbLeftFrame, byte *pbRightFrame, i32 iPelsAvailLeft, i32 iPelsAvailRight,
		i32 iPelsAvailTop, i32 iPelsAvailBottom);

	/**
	*	Set block size.
	*	A block is used as the basic entity for search.
	*/
	void	SetBlkSize(i32 iBlkSize){m_iBlkSize = iBlkSize;}

	/**
	*	Get time for processing.
	*	The time is in msecs.
	*/
	u32		GetTimePerFrame(){return m_uiTime;}

	/**
	*	Get number of SADs.
	*	This is for a complete fraome.
	*/
	i32		GetNumSAD(){return m_iNumSADs;}

	/**
	*	Get MVs arrays.
	*	Motion vectors are generated by calling MotionEstimation function.
	*/
	void	GetMV(i8 **pbMVX, i8 **pbMVY);
	
	/**
	*	Get MVs by block index.
	*	Motion vectors are generated by calling MotionEstimation function.
	*/
	void	GetMV(i32 iBlkIdx, i8 & iMVX, i8 & iMVY);
	
	/**
	*	Get MVs by pixel location.
	*	Motion vectors are generated by calling MotionEstimation function.
	*/
	void	GetMV(i32 iX, i32 iY, i8 & iMVX, i8 & iMVY);

	/**
	*	Image size in blocks.
	*/
	i32		GetImgSizeInBlks(){return m_iImgWidthInBlks*m_iImgHeightInBlks;}
};

#endif	// __RECME_H__