#include <math.h>

typedef struct {
    double x;
    double y;
} Vector;

Vector vector_add(Vector v1, Vector v2);
void vector_iadd(Vector * v1, Vector * v2);
Vector vector_sub(Vector v1, Vector v2);
void vector_isub(Vector * v1, Vector * v2);
double vector_length(Vector v);
double vector_dot(Vector v1, Vector v2);
void vector_normalise(Vector * v);
void vector_normalise_c(Vector * v, double length);
double vector_projection_length(Vector A, Vector B, Vector C);
