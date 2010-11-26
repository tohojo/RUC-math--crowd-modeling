#include <Python.h>
#include <math.h>
#include <pthread.h>
#include "vector.h"

/*** Calculation part begin ***/

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

static void calculate_forces(Py_ssize_t i);
static void add_desired_acceleration(Actor * a);
static void add_repulsion(Actor * a, Actor * b);
static void update_position(Actor * a);
static int is_escaped(Actor * a);

/*** Calculation part end ***/


// For dividing work in threads
typedef struct {
    int start;
    int end;
} Part;

static PyObject * update_actors(PyObject * self, PyObject * args);
static PyObject * add_actors(PyObject * self, PyObject * args);
static PyObject * get_actor(PyObject * self, PyObject * args);
static PyObject * get_actors(PyObject * self, PyObject * args);
static Actor actor_from_pyobject(PyObject * o, Actor * a);
static Py_ssize_t ssize_t_from_attribute(PyObject * o, char * name);
static double double_from_attribute(PyObject * o, char * name);
static Vector vector_from_attribute(PyObject * o, char * name);
static Vector vector_from_pyobject(PyObject * o);
static void cleanup();
static void init_threads();
static void init_walls(PyObject * p_walls);
static void destroy_threads();
static void do_calculations();
static void do_calculation_part(Part * p);
static void check_escapes();
