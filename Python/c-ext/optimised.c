#include "optimised.h"

static double A_1, A_2, B_1, B_2, timestep;
static Py_ssize_t use_threads;

// Global objects to allow access from different threads
static Actor * actors;
static Wall * walls;
static Py_ssize_t a_count;
static Py_ssize_t w_count;

// Threading variables
static pthread_t * threads;
static pthread_attr_t thread_attr;

static PyObject * update_actors(PyObject * self, PyObject * args)
{

    // Since we are not touching any python objects in this part, 
    // we can release the global interpreter lock, to allow for multithreaded
    // goodness.
    Py_BEGIN_ALLOW_THREADS

        do_calculations();

    Py_END_ALLOW_THREADS

    Py_RETURN_NONE;
}

static PyObject * add_actors(PyObject * self, PyObject * args)
{
    PyObject * p_actor_list;
    int i;

    PyArg_ParseTuple(args, "O:add_actors", &p_actor_list);

    for(i = 0; i < a_count; i++) {
        PyObject * p_a = PyList_GetItem(p_actor_list, i);
        actor_from_pyobject(p_a, &actors[i]);
    }
    Py_RETURN_NONE;
}

static PyObject * get_actor(PyObject * self, PyObject * args)
{
    Py_ssize_t i;

    PyArg_ParseTuple(args, "i:get_actor", &i);

    return Py_BuildValue("ddd", 
            actors[i].position.x, actors[i].position.y, actors[i].radius);
}

static void do_calculations()
{
    int i, rc;
    void * status;
    if(use_threads) {
        Part * parts;
        parts = PyMem_Malloc(use_threads * sizeof(Part));
        int part_len = a_count / use_threads;
        for(i = 0; i < use_threads; i++) {
            parts[i].start = i*part_len;
            parts[i].end = (i+1)*part_len;
        }
        parts[use_threads-1].end += a_count % use_threads;

        for(i = 0; i < use_threads; i++) {
            rc = pthread_create(&threads[i], NULL, 
                    do_calculation_part, (void *) &parts[i]);
        }

        for(i = 0; i < use_threads; i++) {
            pthread_join(threads[i], &status);
        }
    } else {
        Part p = {0, a_count};
        do_calculation_part(&p);
    }

    for(i = 0; i < a_count; i++) {
        update_position(&actors[i]);
    }
}

static void do_calculation_part(Part * p)
{
    int i,j;
    for(i = p->start; i < p->end; i++) {
        add_desired_acceleration(&actors[i]);

        for(j = 0; j < a_count; j++) {
            if(i == j) continue;
            add_repulsion(&actors[i], &actors[j]);
        }
    }
    if(use_threads) pthread_exit(NULL);
}

static void add_desired_acceleration(Actor * a)
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

    a->acceleration = towards_target;

}

void add_repulsion(Actor * a, Actor * b)
{
    /* Equivalent Python code:
     
            radius_sum = b.radius + self.radius

            from_b = self.position - b.position
            distance = from_b.length()

            from_b.normalize(distance)
            from_b *= pm.constants.a_2 * \
                    numpy.exp((radius_sum-distance)/pm.constants.b_2)

    */

    double radius_sum = a->radius + b->radius;
    Vector from_b     = vector_sub(a->position, b->position);
    double distance   = vector_length(from_b);
    //if(isnan(distance)) return;

    vector_normalise(&from_b);
    vector_imul(&from_b, A_2 * exp((radius_sum-distance)/B_2));

    vector_iadd(&a->acceleration, &from_b);
}

void update_position(Actor * a)
{
    /* Equivalent Python code:
        # Calculate displacement from acceleration and velocity
        delta_p = Vector(
                self.velocity.x * timestep + 0.5 * self.acceleration.x * timestep**2,
                self.velocity.y * timestep + 0.5 * self.acceleration.y * timestep**2)

        # Update position and velocity, and reset the acceleration
        self.position += delta_p
        self.velocity += self.acceleration
        self.time += timestep
    */

    Vector delta_p;

    delta_p.x = a->velocity.x * timestep + 0.5 * a->acceleration.x * pow(timestep, 2);
    delta_p.y = a->velocity.y * timestep + 0.5 * a->acceleration.y * pow(timestep, 2);


    vector_iadd(&a->position, &delta_p);
    vector_iadd(&a->velocity, &a->acceleration);
    a->time += timestep;
}

void update_python_objects(Actor * actors, PyObject ** p_actors, Py_ssize_t n)
{
    int i;
    for(i = 0; i < n; i++) {
        PyObject * update_p_res;
        PyObject * update_v_res;
        PyObject * update_t_res;

        update_p_res = PyObject_CallMethod(p_actors[i], "set_position", "dd",
                actors[i].position.x, actors[i].position.y);
        update_v_res = PyObject_CallMethod(p_actors[i], "set_velocity", "dd",
                actors[i].velocity.x, actors[i].velocity.y);
        update_t_res = PyObject_CallMethod(p_actors[i], "set_time", "(d)",
                actors[i].time);

        Py_DECREF(update_p_res);
        Py_DECREF(update_v_res);
        Py_DECREF(update_t_res);
    }
}

static Actor actor_from_pyobject(PyObject * o, Actor * a)
{
    a->radius                   = double_from_attribute(o, "radius");
    a->time                     = double_from_attribute(o, "time");
    a->initial_desired_velocity = double_from_attribute(o, "initial_desired_velocity");
    a->max_velocity             = double_from_attribute(o, "max_velocity");
    a->relax_time               = double_from_attribute(o, "relax_time");


    a->position         = vector_from_attribute(o, "position");
    a->initial_position = vector_from_attribute(o, "initial_position");
    a->target           = vector_from_attribute(o, "target");
    a->velocity         = vector_from_attribute(o, "velocity");
    a->acceleration     = vector_from_attribute(o, "acceleration");
}

static Py_ssize_t ssize_t_from_attribute(PyObject * o, char * name)
{
    PyObject * o2 = PyObject_GetAttrString(o, name);
    Py_ssize_t result = PyInt_AsSsize_t(o2);
    Py_DECREF(o2);
    return result;
}

static double double_from_attribute(PyObject * o, char * name)
{
    PyObject * o2 = PyObject_GetAttrString(o, name);
    double result = PyFloat_AsDouble(o2);
    Py_DECREF(o2);
    return result;
}

static Vector vector_from_attribute(PyObject * o, char * name)
{
    PyObject * o2 = PyObject_GetAttrString(o, name);
    Vector result = vector_from_pyobject(o2);
    Py_DECREF(o2);
    return result;
}

static Vector vector_from_pyobject(PyObject * o)
{
    Vector v;

    PyObject * x = PyObject_GetAttrString(o, "x");
    PyObject * y = PyObject_GetAttrString(o, "y");
    v.x = PyFloat_AsDouble(x);
    v.y = PyFloat_AsDouble(y);

    Py_DECREF(x);
    Py_DECREF(y);

    return v;
}

static PyMethodDef OptimisedMethods[] = {
    {"update_actors", update_actors, METH_VARARGS, 
        "Calculate the acceleration of an actor"},
    {"add_actors", add_actors, METH_VARARGS, 
        "Add actors to the list"},
    {"get_actor", get_actor, METH_VARARGS, 
        "Get an actor's position and radius"},
};

PyMODINIT_FUNC initoptimised(void)
{
    PyObject * p_module;
    PyObject * p_constants;
    PyObject * p_actors;
    PyObject * p_walls;

    (void) Py_InitModule("optimised", OptimisedMethods);
    Py_AtExit(cleanup);

    p_module    = PyImport_ImportModule("parameters");
    p_constants = PyObject_GetAttrString(p_module, "constants");
    p_actors    = PyObject_GetAttrString(p_module, "actor");
    p_walls     = PyObject_GetAttrString(p_module, "walls");
    A_2         = double_from_attribute(p_constants, "a_2");
    B_2         = double_from_attribute(p_constants, "b_2");
    timestep    = double_from_attribute(p_module, "timestep");
    use_threads = ssize_t_from_attribute(p_module, "use_threads");
    a_count     = ssize_t_from_attribute(p_actors, "initial_number");

    actors   = PyMem_Malloc(a_count * sizeof(Actor));

    init_walls(p_walls);

    Py_DECREF(p_module);
    Py_DECREF(p_constants);
    Py_DECREF(p_actors);
    Py_DECREF(p_walls);

    if(use_threads) init_threads();
}

static void init_walls(PyObject * p_walls)
{
    int i;
    w_count = PyList_Size(p_walls);
    walls    = PyMem_Malloc(w_count * sizeof(Wall));
    for(i = 0; i < w_count; i++) {
        PyObject * p_w   = PyList_GetItem(p_walls, i);
        walls[i].start.x = PyFloat_AsDouble(PyTuple_GetItem(p_w, 0));
        walls[i].start.y = PyFloat_AsDouble(PyTuple_GetItem(p_w, 1));
        walls[i].end.x   = PyFloat_AsDouble(PyTuple_GetItem(p_w, 2));
        walls[i].end.y   = PyFloat_AsDouble(PyTuple_GetItem(p_w, 3));
    }
}

static void cleanup()
{
    if(use_threads) destroy_threads();
}

static void init_threads()
{
    threads = PyMem_Malloc(use_threads * sizeof(pthread_t));
    pthread_attr_init(&thread_attr);
    pthread_attr_setdetachstate(&thread_attr, PTHREAD_CREATE_JOINABLE);

}

static void destroy_threads()
{
    pthread_attr_destroy(&thread_attr);
    PyMem_Free(threads);
}
