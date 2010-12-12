#include "vector.h"

Vector vector_add(Vector v1, Vector v2)
{
    Vector v;

    v.x = v1.x+v2.x;
    v.y = v1.y+v2.y;

    return v;
}

void vector_iadd(Vector * v1, Vector * v2)
{
    v1->x += v2->x;
    v1->y += v2->y;
}

Vector vector_sub(Vector v1, Vector v2)
{
    Vector v;

    v.x = v1.x-v2.x;
    v.y = v1.y-v2.y;

    return v;
}

void vector_isub(Vector * v1, Vector * v2)
{
    v1->x -= v2->x;
    v1->y -= v2->y;
}

Vector vector_mul(Vector v, double s)
{
    Vector v2;

    v2.x = v.x*s;
    v2.y = v.y*s;

    return v2;
}

void vector_imul(Vector * v, double s)
{
    v->x *= s;
    v->y *= s;
}

double vector_length(Vector v)
{
    return sqrt(v.x*v.x + v.y*v.y);
}

double vector_dot(Vector v1, Vector v2)
{
    return v1.x*v2.x + v1.y*v2.y;
}

void vector_unitise(Vector * v)
{
    double l = vector_length(*v);
    vector_unitise_c(v, l);
}

void vector_unitise_c(Vector * v, double length)
{
    v->x /= length;
    v->y /= length;
}

/**
 * Calculate the projection of C unto the vector pointing from A to B,
 * returning the length along AB that this point is found.
 */
double vector_projection_length(Vector A, Vector B, Vector C)
{
    vector_isub(&C, &A); // Turn C into AC
    vector_isub(&B, &A); // Turn B into AB
    return vector_dot(C, B)/vector_length(B); // AC . AB / |AB|
}

/**
 * Calculate the distance from the line AB to the point C
 */
double vector_projection_distance(Vector A, Vector B, Vector C)
{
    Vector AB, proj;
    double p;
    AB = vector_sub(B, A);
    p = vector_projection_length(A, B, C)/vector_length(AB);
    proj = vector_add(A, vector_mul(AB, p));
    return vector_length(vector_sub(proj, C));
}

int vector_equals(Vector v1, Vector v2) {
    return (v1.x == v2.x && v1.y == v2.y);
}
