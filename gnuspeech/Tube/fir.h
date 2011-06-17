/*******************************************************************************
 *
 *  Copyright (c) 1991-2009 David R. Hill, Leonard Manzara, Craig Schock
 *  
 *  Contributors: Steve Nygard
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 *******************************************************************************
 *
 *  fir.h
 *  Tube
 *
 *  Version: 1.0.1
 *
 ******************************************************************************/

#ifndef __FIR_H
#define __FIR_H

/*  OVERSAMPLING FIR FILTER CHARACTERISTICS  */
#define FIR_BETA                  .2
#define FIR_GAMMA                 .1
#define FIR_CUTOFF                .00000001

/*  VARIABLES FOR FIR LOWPASS FILTER  */
typedef struct {
    double *FIRData, *FIRCoef;
    int FIRPtr, numberTaps;
} TRMFIRFilter;

TRMFIRFilter *TRMFIRFilterCreate(double beta, double gamma, double cutoff);
void TRMFIRFilterFree(TRMFIRFilter *filter);

double FIRFilter(TRMFIRFilter *filter, double input, int needOutput);


#endif
