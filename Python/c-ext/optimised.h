#include <Python.h>

typedef struct {
    double x;
    double y;
} Vector;

typedef struct {
    double radius;
    Vector position;
} Actor;

typedef struct {
    Vector start;
    Vector end;
} Wall;

static PyObject * calculate_acceleration(PyObject * self, PyObject * args);
static Actor actor_from_pyobject(PyObject * o);
static Vector vector_from_pyobject(PyObject * o);
