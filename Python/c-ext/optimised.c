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


    add_desired_acceleration(&a, &acceleration);


    free(actors);
    free(walls);

    return Py_BuildValue("dd", acceleration.x, acceleration.y);
}

static Actor actor_from_pyobject(PyObject * o)
{
    Actor a;

    a.radius = double_from_attribute(o, "radius");
    a.time = double_from_attribute(o, "time");
    a.initial_desired_velocity = double_from_attribute(o, "initial_desired_velocity");
    a.max_velocity = double_from_attribute(o, "max_velocity");
    a.relax_time = double_from_attribute(o, "relax_time");

    a.position = vector_from_attribute(o, "position");
    a.initial_position = vector_from_attribute(o, "initial_position");
    a.target = vector_from_attribute(o, "target");
    a.velocity = vector_from_attribute(o, "velocity");

    return a;
}

static double double_from_attribute(PyObject * o, char * name)
{
    PyObject * o2 = PyObject_GetAttr(o, Py_BuildValue("s", name));
    return PyFloat_AsDouble(o2);
}

static Vector vector_from_attribute(PyObject * o, char * name)
{
    PyObject * o2 = PyObject_GetAttr(o, Py_BuildValue("s", name));
    return vector_from_pyobject(o2);
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

static void add_desired_acceleration(Actor * a, Vector * acceleration)
{
    /* Equivalent Python code:
     
        # To compute the impatience factor, we need the average velocity,
        # in the direction of desired movement.
        #
        # This is found by projecting the direction we have moved onto the
        # vector from the initial position to the target and computing the
        # distance from this projection. The distance travelled is then
        # converted to an average velocity my dividing with the time
        if self.time == 0.0:
            average_velocity = 0.0
        else:
            proj = Vector.projection_length(
                       self.initial_position, self.target, self.position)


            average_velocity = proj / self.time

        # The impatience factor is given by the average velocity divided
        # by the *initial* desired velocity. (6) in the article
        impatience = 1.0 - average_velocity / self.initial_desired_velocity

        # (5) in the article
        desired_velocity = (1.0-impatience) * self.initial_desired_velocity + \
                impatience * self.max_velocity

        towards_target = (self.target - self.position).normal()

        #desired_acceleration = (1.0/self.relax_time) * \
                #(desired_velocity * towards_target - self.velocity)
        towards_target *= desired_velocity
        towards_target -= self.velocity
        towards_target *= (1.0/self.relax_time)

        self.acceleration = towards_target
        */

    double average_velocity, impatience, desired_velocity = 0.0;
    Vector towards_target = {0.0, 0.0};

    if(a->time) {
        double proj = vector_projection_length(
                a->initial_position, a->target, a->position);
        average_velocity = proj / a->time;
    }

    impatience = 1.0 - average_velocity / a->initial_desired_velocity;

    desired_velocity = (1.0-impatience) * a->initial_desired_velocity + \
                       impatience * a->max_velocity;
    towards_target = vector_sub(a->target, a->position);
    vector_normalise(&towards_target);

    vector_imul(&towards_target, desired_velocity);
    vector_isub(&towards_target, &a->velocity);
    vector_imul(&towards_target, 1.0/a->relax_time);

    acceleration->x = towards_target.x;
    acceleration->y = towards_target.y;

}

static PyMethodDef OptimisedMethods[] = {
    {"calculate_acceleration", calculate_acceleration, METH_VARARGS, 
        "Calculate the acceleration of an actor"},
};

PyMODINIT_FUNC initoptimised(void)
{
    (void) Py_InitModule("optimised", OptimisedMethods);
}

