#include <Python.h>

static PyObject * test(PyObject * self, PyObject * args)
{
    return Py_BuildValue("s", "testing");
}

static PyMethodDef OptimisedMethods[] = {
    {"test", test, METH_VARARGS, "Test function"},
};

PyMODINIT_FUNC initoptimised(void)
{
    (void) Py_InitModule("optimised", OptimisedMethods);
}

