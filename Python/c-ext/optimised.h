#include <Python.h>
#include <math.h>
#include "vector.h"


typedef struct {
    double radius;
    double time;
    double initial_desired_velocity;
    double max_velocity;
    double relax_time;
    Vector position;
    Vector initial_position;
    Vector target;
    Vector velocity;
} Actor;

typedef struct {
    Vector start;
    Vector end;
} Wall;

static PyObject * calculate_acceleration(PyObject * self, PyObject * args);
static Actor actor_from_pyobject(PyObject * o);
static double double_from_attribute(PyObject * o, char * name);
static Vector vector_from_attribute(PyObject * o, char * name);
static Vector vector_from_pyobject(PyObject * o);
static void add_desired_acceleration(Actor * a, Vector * acceleration);
static void add_repulsion(Actor * a, Actor * b, Vector * acceleration);
