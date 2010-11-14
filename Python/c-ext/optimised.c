#include "optimised.h"


static PyObject * calculate_acceleration(PyObject * self, PyObject * args)
{
    // Python objects
    PyObject * p_this; // Calling actor
    PyObject * p_actors; // List of other actors
    PyObject * p_walls; // List of walls

    // Native objects
    Actor * actors;
    Wall * walls;
    Actor a;

    Vector acceleration = {0.0, 0.0};

    int i;

    PyArg_ParseTuple(args, "OOO:calculate_acceleration", &p_this, &p_actors, &p_walls);

    // The actors also contain the current actor, so we need to store one
    // less actor than the number passed
    Py_ssize_t a_count = PyList_Size(p_actors) -1;
    Py_ssize_t w_count = PyList_Size(p_walls);

    actors = malloc(a_count * sizeof(Actor));
    walls = malloc(w_count * sizeof(Wall));

    a = actor_from_pyobject(p_this);

    for(i = 0; i < a_count; i++) {
        PyObject * p_a = PyList_GetItem(p_actors, i);

        if(PyObject_Compare(p_this, p_a) != 0) {
            actors[i] = actor_from_pyobject(p_a);
        }
    }




    free(actors);
    free(walls);

    return Py_BuildValue("dd", acceleration.x, acceleration.y);
}

static Actor actor_from_pyobject(PyObject * o)
{
    Actor a;

    PyObject * radius = PyObject_GetAttr(o, Py_BuildValue("s", "radius"));
    a.radius = PyFloat_AsDouble(radius);

    PyObject * position = PyObject_GetAttr(o, Py_BuildValue("s", "position"));

    a.position = vector_from_pyobject(position);

    return a;
}

static Vector vector_from_pyobject(PyObject * o)
{
    Vector v;

    PyObject * x = PyObject_GetAttr(o, Py_BuildValue("s", "x"));
    v.x = PyFloat_AsDouble(x);
    PyObject * y = PyObject_GetAttr(o, Py_BuildValue("s", "y"));
    v.y = PyFloat_AsDouble(y);

    return v;
}

static PyMethodDef OptimisedMethods[] = {
    {"calculate_acceleration", calculate_acceleration, METH_VARARGS, 
        "Calculate the acceleration of an actor"},
};

PyMODINIT_FUNC initoptimised(void)
{
    (void) Py_InitModule("optimised", OptimisedMethods);
}

