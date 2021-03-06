# Copyright (C) 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# 


## 
# @file sample_apx_space_and_run.py
# @brief this file contains all the modules responsible for sampling the apx_op_space (generated by src_parse_and_apx_op_space_gen) and running them
# @author Behzad Boroujerdian
# @date 2015-07-01

import os
from make_run import make_run
import settings


def modifyOperatorSampleFile(operatorSampleFileFullAddress, setUp):
    operatorSampleFileNameP = open(operatorSampleFileFullAddress, "w")
    for operator in setUp:
        for property in operator:
            operatorSampleFileNameP.write(str(property).replace(',', ' ') + " ")
        
        operatorSampleFileNameP.write("\n")

    operatorSampleFileNameP.close()
    
    
