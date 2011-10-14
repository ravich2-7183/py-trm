%module gnuspeech

%{
#include <Tube/TubeModel.h>
%}

%include "carrays.i"
%array_functions(double, double_array);

%typemap(memberin) double [10][2][2] {
    memmove($1, $input, 10 * 2 * 2 * sizeof(double));
}

%typemap(memberin) double [6][2][2] {
    memmove($1, $input, 6 * 2 * 2 * sizeof(double));
}

%typemap(memberin) TRMInputParameters {
    $1 = *($input);
    memmove($1.noseRadius, $input->noseRadius, TOTAL_NASAL_SECTIONS * sizeof(double));
}

%typemap(out) FILE * {
    $result = PyFile_FromFile($1, "__temp__", "r", NULL);
}

%include <Tube/input.h>
%include <Tube/output.h>
%include <Tube/structs.h>
%include <Tube/tube.h>
