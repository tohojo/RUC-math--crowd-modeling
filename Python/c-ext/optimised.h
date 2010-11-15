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
    Vector acceleration;
} Actor;

typedef struct {
    Vector start;
    Vector end;
} Wall;

static PyObject * update_actors(PyObject * self, PyObject * args);
static Actor actor_from_pyobject(PyObject * o);
static Py_ssize_t ssize_t_from_attribute(PyObject * o, char * name);
static double double_from_attribute(PyObject * o, char * name);
static Vector vector_from_attribute(PyObject * o, char * name);
static Vector vector_from_pyobject(PyObject * o);
static void add_desired_acceleration(Actor * a);
static void add_repulsion(Actor * a, Actor * b);
static void update_position(Actor * a);
static void update_python_objects(Actor * actors, PyObject ** p_actors, Py_ssize_t n);
