#include <Python.h>
#include <math.h>
#include "vector.h"
#ifndef _WIN32
#include <pthread.h>
#endif

/*** Calculation part begin ***/

typedef struct {
    double radius;
    double time;
    double initial_desired_velocity;
    double max_velocity;
    double relax_time;
	int flowline[5];
    Vector position;
    Vector initial_position;
    Vector target;
    Vector velocity;
    Vector acceleration;
} Pedestrian;

typedef struct {
    Vector start;
    Vector end;
    double length;
} Wall;

static void calculate_forces(Py_ssize_t i);
static void add_desired_acceleration(Pedestrian * a);
static Vector calculate_repulsion(Pedestrian * a, Pedestrian * b, double A, double B);
static void add_repulsion(Pedestrian * a, Pedestrian * b);
static void add_social_sphere(Pedestrian * a, Pedestrian * b);
static void add_wall_repulsion(Pedestrian * a);
static int find_repulsion_points(Pedestrian * a, Vector repulsion_points[]);
static Vector calculate_wall_repulsion(Pedestrian * a, Vector repulsion_point);
static void update_position(Pedestrian * a);
static int is_escaped(Pedestrian * a);
static void check_flowlines(Pedestrian * a);

#define ESCAPE_THRESHOLD 50

/*** Calculation part end ***/


// For dividing work in threads
typedef struct {
    int start;
    int end;
} Part;

static PyObject * update_pedestrians(PyObject * self, PyObject * args);
static PyObject * add_pedestrian(PyObject * self, PyObject * args);
static PyObject * a_property(PyObject * self, PyObject * args);
static PyObject * set_parameters(PyObject * self, PyObject * args);
static PyObject * flow_count(PyObject * self, PyObject * args);
static void pedestrian_from_pyobject(PyObject * o, Pedestrian * a);
static Wall wall_from_pyobject(PyObject * o);
static Py_ssize_t ssize_t_from_attribute(PyObject * o, char * name);
static double double_from_attribute(PyObject * o, char * name);
static Vector vector_from_attribute(PyObject * o, char * name);
static Vector vector_from_pyobject(PyObject * o);
static void cleanup();
static void init_threads();
static void init_walls(PyObject * p_walls, Wall * walls, Py_ssize_t w_count);
static void destroy_threads();
static void do_calculations();
static void do_calculation_part(Part * p);
static void check_escapes();
static void update_a_count(Py_ssize_t count);
